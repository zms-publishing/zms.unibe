import importlib
import pkgutil
import os

from fastapi import FastAPI
from redis import Redis
from rq import Queue
from rq_dashboard_fast import RedisQueueDashboard
from contextlib import asynccontextmanager

from Products.zms.standard import pybool

import zms.unibe.fastapi as endpoints


# https://stackoverflow.com/questions/3365740/how-to-import-all-submodules#65021760
def import_submodules_recursively(module):
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            module.__path__, module.__name__ + '.'):
        importlib.import_module(module_name)

# https://fastapi.tiangolo.com/#run-it
# https://fastapi.tiangolo.com/fastapi-cli/
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#enable-proxy-forwarded-headers
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#mounting-a-sub-application
# https://fastapi.tiangolo.com/advanced/events/#sub-applications
# Please note:
# - The proxy_headers and the forwarded_allow_ips must be set for all mounted sub-applications as well.
# - The ignore_trailing_slashes and to not redirect_slashes must be set for all mounted sub-applications as well.
# - Keep in mind that lifespan events (startup and shutdown) will only be executed for the main application,
#   not for mounted sub-applications.

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CONN = None
RQ_NAME = os.getenv("RQ_NAME", "default")
RQ_JOBS = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    global REDIS_HOST, REDIS_PORT, REDIS_CONN
    global RQ_NAME, RQ_JOBS
    try:
        if pybool(os.getenv("API_RQ")):
            REDIS_CONN = Redis(host=REDIS_HOST, port=REDIS_PORT)
            RQ_JOBS = Queue(RQ_NAME, connection=REDIS_CONN)
            print(f"    connected: RQ queue '{RQ_NAME}' at redis://{REDIS_HOST}:{REDIS_PORT}")
        yield
    except Exception as e:
        print("ERROR:", e)
        yield
    finally:
        if REDIS_CONN:
            REDIS_CONN.close()

api = FastAPI(
    openapi_url=None,
    proxy_headers=True,
    forwarded_allow_ips=["*"],
    ignore_trailing_slashes=True,
    redirect_slashes=False,
    lifespan=lifespan,
)

if pybool(os.getenv("API_RQ")):
    dashboard = RedisQueueDashboard(f"redis://{REDIS_HOST}:{REDIS_PORT}", 
                                    "/rq-dashboard")
    api.mount("/rq-dashboard", dashboard)

import_submodules_recursively(endpoints)
