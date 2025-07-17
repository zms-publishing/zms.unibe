import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse

from cmsapi.mobileapp.metadata import tags
from cmsapi.mobileapp.routers import newsevents, servicelinks, uniaktuell, mediareleases

app = FastAPI(title="CMSAPI-v3 for unibe.app",
              version="3.3.0",
              description="Python-based REST API for unibe.app "
                          "to aggregate and provide "
                          "News, Events, Announcements and Service Links.",
              docs_url="/v3/swagger",
              redoc_url="/v3/redoc",
              openapi_url="/v3/openapi.json",
              openapi_tags=tags,
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})

origins = [
    "http://localhost:63342",  # TODO: adjust CORS hosts/ports
    "http://127.0.0.1:63342",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(newsevents.router)
app.include_router(uniaktuell.router)
app.include_router(mediareleases.router)
app.include_router(servicelinks.router)


@app.get("/v3", include_in_schema=False)
def redirect_docs():
    return RedirectResponse("/v3/swagger")


@app.get("/v3/healthcheck", include_in_schema=False)
def check_health():
    return PlainTextResponse("OK", 200)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5003)
