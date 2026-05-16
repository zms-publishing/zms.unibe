import os
from uuid import UUID

import xmltodict
from fastapi import APIRouter, Query, Response, HTTPException

# TODO: this is an example to prove the concept with ZMSAgendaResponse
from zms.unibe.agenda.schemas import ZMSAgendaSchema as schema
from zms.unibe.agenda.schemas.ZMSAgendaEventSchema import ZMSAgendaEventSchema
from zms.unibe.fastapi.meta import Tags
from zms.unibe.utils.enums import ContentModel, ImageVariant, Lang, Locale
from zms.unibe.utils.helpers import get_data, is_activated_by_checkbox_and_timeline
from zms.unibe.utils.zope.context import create_zope_app_context, get_zmsindex

router = APIRouter(prefix="/zms/content", tags=[Tags.content])

@router.get(
    path="/objects",
    summary="Get content objects by model type and filtered by path",
)
def get_content_objects(
        locale: Locale = Locale.de,
        content_model: ContentModel | None = None,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
        path_filter: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                        description="Filter by path"),
        offset: int = 0,
        limit: int = 20,
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    
    results = zmsindex({
        "meta_id": content_model,
        "path": path_filter,
    })
    
    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)

    # TODO: filter out inactive by attribute and context

    objs = [xmltodict.parse(x.getObject().toXml(
        REQUEST=context.REQUEST,
        deep=False,
        data2hex=False,
        multilang=False,
    )) for x in results[offset : offset + limit]]

    return {
        'offset': offset,
        'limit': limit,
        'total': len(results),
        'locale': locale.value,
        'portal_master': portal_master,
        'path_filter': path_filter,
        'content_model': content_model,
        'content_objects': objs,
    }


@router.get(
    path="/object/{uuid}",
    summary="Get attributes of the given content object uuid",
)
def get_content_object_by_uuid(
        uuid: UUID,
        locale: Locale = Locale.de,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    
    results = zmsindex({ 
        "get_uid": f"uid:{uuid}",
    })

    if len(results) == 0:
        raise HTTPException(status_code=404,
                            detail=f"Object with uuid '{uuid}' not found")

    if len(results) > 1:
        raise HTTPException(status_code=500,
                            detail=f"Multiple objects found for uuid '{uuid}'")
    
    entry = results[0]
    obj = entry.getObject()
    meta_id = entry.meta_id

    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)
    
    obj = xmltodict.parse(obj.toXml(
        REQUEST=context.REQUEST,
        deep=False,
        data2hex=False,
        multilang=False,
    ))
    
    return obj[meta_id]


@router.get(
    path="/object/{uuid}/data",
    summary="Get data stored for the given content object uuid",
    response_model=schema.ZMSAgendaResponse  # TODO: handle appropriate response_model according to the processed content_object
)
def get_content_object_data_by_uuid(
        uuid: UUID,
        locale: Locale = Locale.de,
        portal_master: str | None = Query(os.getenv('PORTAL_MASTER', '/myzmsx/content'),
                                          description="Portal master with ZMSIndex"),
        image_variant: ImageVariant = ImageVariant.img,
        include_schema: bool = False,
        offset: int = 0,
        limit: int = 20,
):
    context = create_zope_app_context()
    zmsindex = get_zmsindex(portal_master, context)
    
    results = zmsindex({
        "get_uid": f"uid:{uuid}",
    })
    
    if len(results) == 0:
        raise HTTPException(status_code=404,
                            detail=f"Object with uuid '{uuid}' not found")

    if len(results) > 1:
        raise HTTPException(status_code=500,
                            detail=f"Multiple objects found for uuid '{uuid}'")
    
    entry = results[0]
    obj = entry.getObject()
    meta_id = entry.meta_id
    site_path = entry.getPath()

    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)

    if not is_activated_by_checkbox_and_timeline(obj, lang):
        raise HTTPException(status_code=404,
                            detail=f"Object with uuid '{uuid}' is not activated")

    attr = "file"
    if meta_id in ContentModel._member_names_:
        if meta_id in ("ZMSDataTable", "ZMSBoris", "ZMSAgenda"):
            attr = "_datafilecached"
        elif meta_id == "ZMSGraphic":
            attr = image_variant.value

    data, headers = get_data(obj, attr, lang=lang, json_as_py=True)
    
    if data is None or headers is None:
        raise HTTPException(status_code=404,
                            detail=f"Object with uuid '{uuid}' has no '{attr}' data")
    
    if isinstance(data, list):
        return {
            'offset': offset,
            'limit': limit,
            'total': len(data),
            'locale': locale.value,
            'site_path': site_path,
            'content_model': meta_id,
            # TODO: handle appropriate data_schema according to the processed content_object
            'data_schema': ZMSAgendaEventSchema.model_json_schema() if include_schema else None,
            'data_items': data[offset : offset + limit],
        }

    return Response(data,
                    headers=headers,
                    media_type=headers['Content-Type'])
