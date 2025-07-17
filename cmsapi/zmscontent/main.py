import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse

from cmsapi.zmscontent.metadata import tags
from cmsapi.zmscontent.routers import zmscontent, zmsobjects

app = FastAPI(title="CMSAPI-v1 for unibe.ch",
              version="1.0.0",
              description="Python-based REST API for unibe.ch "
                          "to retrieve and analyze "
                          "content objects published in UniBE-CMS.",
              docs_url="/v1/swagger",
              redoc_url="/v1/redoc",
              openapi_url="/v1/openapi.json",
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

app.include_router(zmscontent.router)
app.include_router(zmsobjects.router)


@app.get("/v1", include_in_schema=False)
def redirect_docs():
    return RedirectResponse("/v1/swagger")


@app.get("/v1/healthcheck", include_in_schema=False)
def check_health():
    return PlainTextResponse("OK", 200)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5001)
