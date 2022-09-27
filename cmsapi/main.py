import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .metadata import cmsapi_tags
from .routers import zmsmodels, zmsdefaults, newsevents, uniaktuell

app = FastAPI(title="CMSAPI v3 PoC",
              version="3.0.0dev",
              description="REST-API to retrieve data from UniBE CMS",
              openapi_tags=cmsapi_tags,
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.include_router(zmsmodels.router)
app.include_router(zmsdefaults.router)
app.include_router(newsevents.router)
app.include_router(uniaktuell.router)


@app.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse("/docs")


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5003)
