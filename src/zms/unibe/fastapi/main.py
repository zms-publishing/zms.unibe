from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse

from app.main import api
from zms.unibe.fastapi.meta import tags
from .mobileapp import mediareleases, newsevents, servicelinks, uniaktuell
from .zmscontent import agenda, labels, objects, scheduler

# https://fastapi.tiangolo.com/advanced/sub-applications/
v1 = FastAPI(
    title="zms.unibe.fastapi",
    summary="Python-based REST API to connect unibe.ch and unibe.app with ZMS",
    version="1.0.0",
    openapi_tags=tags,
    redoc_url="/redoc",
    servers=[
        {"url": "https://stag.example.com/v1", "description": "Staging environment"},
        {"url": "https://prod.example.com/v1", "description": "Production environment"},
    ]
)
api.mount("/v1", v1)

v3 = FastAPI(
    title="zms.unibe.fastapi",
    summary="Python-based REST API to connect unibe.ch and unibe.app with ZMS",
    version="3.3.3",
    openapi_tags=tags,
    redoc_url="/redoc",
    servers=[
        {"url": "https://stag.example.com/v3", "description": "Staging environment"},
        {"url": "https://prod.example.com/v3", "description": "Production environment"},
    ]
)
api.mount("/v3", v3)


@v1.get("/", include_in_schema=False)
def redirect_docs_v1():
    return RedirectResponse("/v1/docs")


@v3.get("/", include_in_schema=False)
def redirect_docs_v3():
    return RedirectResponse("/v3/docs")


@v1.get("/healthcheck")
@v3.get("/healthcheck")
def check_health():
    return PlainTextResponse("OK", 200)


# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/reference/apirouter/
v1.include_router(objects.router)
v1.include_router(labels.router)
v1.include_router(scheduler.router)
v1.include_router(agenda.router)
v3.include_router(newsevents.router)
v3.include_router(servicelinks.router)
v3.include_router(uniaktuell.router)
v3.include_router(mediareleases.router)
