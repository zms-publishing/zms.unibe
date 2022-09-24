from fastapi import APIRouter, Query
from ..helpers import MetaObj, AttrType, get_zms_model

router = APIRouter(
    prefix="/v3/zms",
    tags=["ZMS Models"]
)


@router.get("/models")
async def get_models(
        metaobj: MetaObj,
        types: list[AttrType] = Query(...)):
    return get_zms_model(
        name=metaobj.value,
        types=[item.value for item in types],
        metas=True)
