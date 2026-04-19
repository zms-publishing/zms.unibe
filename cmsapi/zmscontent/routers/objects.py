from uuid import UUID

import xmltodict
from fastapi import APIRouter, Query
from fastapi.responses import Response

from zms.unibe.utils.zope.context import create_zope_app_context
from zms.unibe.utils.helpers import is_activated_by_checkbox_and_timeline, get_data
from zms.unibe.utils.enums import Locale, Lang, ContentModel, ImageVariant
from zms.unibe.agenda.schemas.ZMSAgendaEventSchema import ZMSAgendaEventSchema
from ..schemas import agenda as schema  # TODO: this is an example to prove the concept with ZMSAgendaResponse


router = APIRouter(
    prefix="/v3/zms",
    tags=["UniBE Web CMS (unibe.ch)"],
)


@router.get(
    path="/content/objects",
    summary="Get content objects by model type and filtered by site path",
)
def get_content_objects(
        locale: Locale = Locale.de,
        content_model: ContentModel | None = None,
        site_path: str | None = Query("/unibe/portal/content", description="Filter by path"),
        offset: int = 0,
        limit: int = 20,
):
    context = create_zope_app_context()
    zmsindex = context.zcatalog_index({
        "meta_id": content_model,
        "path": site_path,
    })
    
    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)

    # TODO: filter out inactive by attribute and context

    objs = [xmltodict.parse(x.getObject().toXml(
        REQUEST=context.REQUEST,
        deep=False,
        data2hex=False,
        multilang=False,
    )) for x in zmsindex[offset : offset + limit]]

    return {
        'offset': offset,
        'limit': limit,
        'total': len(zmsindex),
        'locale': locale.value,
        'site_path': site_path,
        'content_model': content_model,
        'content_objects': objs,
    }


@router.get(
    path="/content/object/{uuid}",
    summary="Get attributes of the given content object uuid",
)
def get_content_object_by_uuid(
        uuid: UUID,
        locale: Locale = Locale.de,
):
    context = create_zope_app_context()
    zmsindex = context.zcatalog_index({ 
        "get_uid": f"uid:{uuid}",
    })
    
    if len(zmsindex) != 1:
        return Response(status_code=404)
    
    entry = zmsindex[0]
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
    path="/content/object/{uuid}/data",
    summary="Get data stored for the given object uuid",
    response_model=schema.ZMSAgendaResponse  # TODO: handle appropriate response_model according to the processed content_object
)
def get_content_object_data_by_uuid(
        uuid: UUID,
        locale: Locale = Locale.de,
        image_variant: ImageVariant = ImageVariant.img,
        include_schema: bool = False,
        offset: int = 0,
        limit: int = 20,
):
    context = create_zope_app_context()
    zmsindex = context.zcatalog_index({
        "get_uid": f"uid:{uuid}",
    })
    
    if len(zmsindex) != 1:
        return Response(status_code=404)
    
    entry = zmsindex[0]
    obj = entry.getObject()
    meta_id = entry.meta_id
    site_path = entry.getPath()

    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)

    if not is_activated_by_checkbox_and_timeline(obj, lang):
        return Response(status_code=404)

    attr = "file"
    if meta_id in ContentModel._member_names_:
        if meta_id in ("ZMSDataTable", "ZMSBoris", "ZMSAgenda"):
            attr = "_datafilecached"
        elif meta_id == "ZMSGraphic":
            attr = image_variant.value

    data, headers = get_data(obj, attr, lang=lang, json_as_py=True)
    
    if data is None or headers is None:
        return Response(status_code=404)
    
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
