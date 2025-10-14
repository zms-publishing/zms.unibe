from uuid import UUID

import xmltodict
import requests
from fastapi import APIRouter, Query
from fastapi.responses import Response
from sqlmodel import Session, select, inspect
from zms.unibe.utils.db import connect_sqldb

from zms.unibe.utils.zope.context import create_zope_app_context
from zms.unibe.utils.helpers import get_url_from_conf_or_env
from zms.unibe.utils.enums import Locale, Lang, ContentModel, ImageVariant
from zms.unibe.maintenance.sqlmodels.ZMSSchedulerRegistry import ZMSSchedulerRegistry
from ..schemas import agendas as schema


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
    obj = zmsindex[0].getObject()
    meta_id = zmsindex[0].meta_id

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
    # response_model=schema.ZMSAgendaResponse
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
    obj = zmsindex[0].getObject()
    meta_id = zmsindex[0].meta_id
    site_path = zmsindex[0].getPath()

    lang = Lang[locale].value
    context.REQUEST.set('lang', lang)
    
    url = get_url_from_conf_or_env(obj)
    attr = "file"
    if meta_id in ContentModel._member_names_:
        if meta_id in ("ZMSDataTable", "ZMSBoris", "ZMSAgenda"):
            attr = "_datafilecached" 
        elif meta_id == "ZMSGraphic":
            attr = image_variant.value

    href = obj.attr(attr).getHref(REQUEST=context.REQUEST) if (obj.attr(attr) is not None) else None
    if href is None:
        raise Exception(f"No data found for {meta_id} at {site_path}")
    
    response = requests.get(url + href)
    if response.status_code != 200:
        raise Exception(f"Error getting data from {url + href}")
    
    if response.apparent_encoding == 'ascii':
        data = response.json()
        return {
            'offset': offset,
            'limit': limit,
            'total': len(data),
            'locale': locale.value,
            'site_path': site_path,
            'content_model': meta_id,
            # TODO: handle appropriate data_schema according to the processed content_object
            'data_schema': schema.ZMSAgendaEventSchema.model_json_schema() if include_schema else None,
            'data_items': data[offset : offset + limit],
        }
    else:        
        return Response(response.content,
                        headers=response.headers,
                        media_type=response.headers['Content-Type'])


@router.post(
    path="/content/agenda/{upn}",
    summary="Schedule update of agenda(s) identified by User Principal Name (UPN)",
)
def schedule_agenda_update_by_upn(
        upn: str,
):
    context = create_zope_app_context()
    zmsindex = context.zcatalog_index({
        "meta_id": "ZMSAgenda",
    })

    sqlengine = connect_sqldb()

    if not inspect(sqlengine).has_table(ZMSSchedulerRegistry.__name__.lower()):
        ZMSSchedulerRegistry.__table__.create(sqlengine)

    with Session(sqlengine) as session:
        for item in zmsindex:  # an UPN may by set for multiple ZMSAgenda objects
            obj = item.getObject()
            if obj.attr('include_outlook') and obj.attr('outlook_upn') == upn:
                session.add(ZMSSchedulerRegistry.from_agenda(obj))
                session.commit()
        
        statement = select(ZMSSchedulerRegistry).where(
            ZMSSchedulerRegistry.task_title == upn).where(
            ZMSSchedulerRegistry.exec_onchange == True).where(
            ZMSSchedulerRegistry.processed_dt.is_(None))
        results = session.exec(statement)
            
        return results.all()
