import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from Products.zms.standard import pybool

from app.main import api
from zms.unibe.fastapi.meta import tags
from .mobileapp import mediareleases, newsevents, servicelinks, uniaktuell
from .zmscontent import labels, managers, objects, scheduler, system

# https://fastapi.tiangolo.com/advanced/sub-applications/
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#enable-proxy-forwarded-headers
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#mounting-a-sub-application
# Please note:
# - The proxy_headers and the forwarded_allow_ips must be set for all mounted sub-applications as well.
# - The ignore_trailing_slashes and to not redirect_slashes must be set for all mounted sub-applications as well.

v1 = FastAPI(
    title="zms.unibe.fastapi",
    summary="Python-based REST API to connect unibe.ch and unibe.app with ZMS",
    version="1.0.1",
    openapi_tags=tags,
    redoc_url="/redoc",
    proxy_headers=True,
    forwarded_allow_ips=["*"],
    ignore_trailing_slashes=True,
    redirect_slashes=False,
    servers=[  # TODO: set urls
        {"url": "https://stag.example.com/v1", "description": "Staging environment"},
        {"url": "https://prod.example.com/v1", "description": "Production environment"},
    ]
)
if pybool(os.getenv("API_V1")):
    api.mount("/v1", v1)

v3 = FastAPI(
    title="zms.unibe.fastapi",
    summary="Python-based REST API to connect unibe.ch and unibe.app with ZMS",
    version="3.4.0",
    openapi_tags=tags,
    redoc_url="/redoc",
    proxy_headers=True,
    forwarded_allow_ips=["*"],
    ignore_trailing_slashes=True,
    redirect_slashes=False,
    servers=[  # TODO: set urls
        {"url": "https://stag.example.com/v3", "description": "Staging environment"},
        {"url": "https://prod.example.com/v3", "description": "Production environment"},
    ]
)
if pybool(os.getenv("API_V3")):
    api.mount("/v3", v3)


@v1.get("/healthcheck")
@v3.get("/healthcheck")
def check_health():
    return PlainTextResponse("OK", 200)


# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/reference/apirouter/
v1.include_router(objects.router)
v1.include_router(labels.router)
v1.include_router(managers.router)
v1.include_router(scheduler.router)
v1.include_router(system.router)
v3.include_router(newsevents.router)
v3.include_router(servicelinks.router)
v3.include_router(uniaktuell.router)
v3.include_router(mediareleases.router)
