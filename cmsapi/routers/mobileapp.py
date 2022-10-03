from fastapi import APIRouter

router = APIRouter(
    prefix="/v3/app",
    tags=["UniBE Mobile App"]
)


@router.get("/contact")  # TODO: add router, model and schema
async def get_app_contact():
    return []


@router.get("/imprint")  # TODO: add router, model and schema
async def get_app_imprint():
    return []


@router.get("/indexaz")  # TODO: add router, model and schema
async def get_app_indexaz():
    return []


@router.get("/locations")  # TODO: add router, model and schema
async def get_app_locations():
    return []


@router.get("/privacypolicy")  # TODO: add router, model and schema
async def get_app_privacypolicy():
    return []


@router.get("/termsofservice")  # TODO: add router, model and schema
async def get_app_termsofservice():
    return []
