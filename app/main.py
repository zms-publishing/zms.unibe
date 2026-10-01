import pkgutil
import os
import traceback

from fastapi import FastAPI
from sqlmodel import SQLModel
from redis import Redis, ConnectionPool
from rq import Queue
from rq_dashboard_fast import RedisQueueDashboard
from contextlib import asynccontextmanager
from pathlib import Path
from importlib import import_module

from zms.unibe.utils.db import connect_sqldb
from Products.zms.standard import pybool

import zms.unibe.fastapi as endpoints

# https://stackoverflow.com/questions/3365740/how-to-import-all-submodules#65021760
def import_submodules_recursively(module):
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            module.__path__, module.__name__ + '.'):
        import_module(module_name)

def import_sqlmodels_recursively():
    """
    Import all Python modules matching:
        ../src/zms/unibe/**/sqlmodels/*.py
    Skips __main__.py and __init__.py.
    Path resolution is based on this file's location.
    """
    root_path = (Path(__file__).resolve().parent.parent / "src/zms/unibe").resolve()
    root_package = "zms.unibe"
    for py_file in root_path.rglob("sqlmodels/*.py"):
        if py_file.name in ("__main__.py", "__init__.py"):
            continue
        rel = py_file.relative_to(root_path).with_suffix("")
        module_name = ".".join((root_package, *rel.parts))
        print("SQLModel:", module_name)
        import_module(module_name)

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
# - The state of the main application must be passed to the mounted sub-applications to access shared resources
#   like database, cache, and queue connections on dependency injection.
#   -> see src/zms/unibe/fastapi/main.py: v1.main_state = api.state | v3.main_state = api.state

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
QUEUE_NAME = os.getenv("QUEUE_NAME", "default")
QUEUE_POOL = ConnectionPool.from_url(REDIS_URL,
                                     db=0,
                                     max_connections=20,
                                     socket_connect_timeout=2.0,  # time to establish the initial connection
                                     socket_timeout=5.0,  # time to wait for individual command responses
                                     decode_responses=False)  # RQ uses bytes for job data
CACHE_POOL = ConnectionPool.from_url(REDIS_URL,
                                     db=1,
                                     max_connections=20,
                                     socket_connect_timeout=2.0,  # time to establish the initial connection
                                     socket_timeout=5.0,  # time to wait for individual command responses
                                     decode_responses=True)  # converts bytes to str for cache data

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        import_submodules_recursively(endpoints)
        import_sqlmodels_recursively()
        app.state.sqldb_engine = connect_sqldb(verbose=True)
        SQLModel.metadata.create_all(app.state.sqldb_engine)
        app.state.redis_cache_conn = Redis(connection_pool=CACHE_POOL)
        if pybool(os.getenv("API_RQ")):
            app.state.redis_queue_conn = Redis(connection_pool=QUEUE_POOL)
            app.state.redis_queue_jobs = Queue(QUEUE_NAME,
                                               connection=app.state.redis_queue_conn)
            print(f"    connected: RQ queue '{QUEUE_NAME}' at {REDIS_URL}")
        yield
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        os._exit(1)  # Bypasses the further exception handling that would occur with sys.exit().
                     # Prevents any cleanup – which is fine in this case, however, since the
                     # error occurred at startup (before yield) – so the app is not yet running
                     # and no resources have been allocated that would need to be cleaned up.
    finally:
        if getattr(app.state, "sqldb_engine", None):
            app.state.sqldb_engine.dispose()
        if getattr(app.state, "redis_cache_conn", None):
            app.state.redis_cache_conn.close()
        if getattr(app.state, "redis_queue_conn", None):
            app.state.redis_queue_conn.close()
        CACHE_POOL.disconnect()
        QUEUE_POOL.disconnect()

api = FastAPI(
    openapi_url=None,
    proxy_headers=True,
    forwarded_allow_ips=["*"],
    ignore_trailing_slashes=True,
    redirect_slashes=False,
    lifespan=lifespan,
)

if pybool(os.getenv("API_RQ")):
    dashboard = RedisQueueDashboard(REDIS_URL, "/rq-dashboard")
    api.mount("/rq-dashboard", dashboard)
