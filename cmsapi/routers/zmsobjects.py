from fastapi import APIRouter, Query
from sqlmodel import Session, select
from ..db import engine

from ..models import zmsobjects as model
from ..schemas import zmsobjects as schema
from ..helpers import Lang, MetaObj, AttrType, get_zms_model, get_attr_by_lang, get_subdomain, strip_cmstest

router = APIRouter(
    prefix="/v3/zms",
    tags=["ZMS Objects"]
)


@router.get("/models", summary='Content Models')
async def get_content_models(
        metaobj: MetaObj,
        types: list[AttrType] = Query(...)):
    return get_zms_model(
        name=metaobj.value,
        types=[item.value for item in types],
        metas=True)


@router.get("/sites", summary='Content Sites', response_model=list[schema.ZMSSite])
async def get_content_sites(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 500):
    with Session(engine) as session:
        statement = select(model.ZMSSite). \
            where(model.ZMSSite.domain != ''). \
            where(get_attr_by_lang(lang,
                                   de=model.ZMSSite.active_de,
                                   en=model.ZMSSite.active_en,
                                   fr=model.ZMSSite.active_fr)). \
            order_by(model.ZMSSite.domain). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.ZMSSite.parse_obj({
                'siteUuid': res.uuid,
                'sitePath': res.path,
                'siteType': res.type,
                'siteShort': get_subdomain(res.domain),
                'siteTitle': get_attr_by_lang(lang, de=res.title_de, en=res.title_en, fr=res.title_fr),
                'siteAlias': ', '.join(strip_cmstest(res.alias).strip().split()),
                'siteDomain': strip_cmstest(res.domain),
            }))
        return rtn


@router.get("/documents/{site}", response_model=list[model.ZMSDocument], include_in_schema=False)  # TODO: router/schema
async def get_documents_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSDocument).join(model.ZMSSite). \
            where(model.ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/folders/{site}", response_model=list[model.ZMSFolder], include_in_schema=False)  # TODO: router/schema
async def get_folders_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSFolder).join(model.ZMSSite). \
            where(model.ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/forms/{site}", summary='Forms by Site', response_model=list[model.ZMSFormulator])  # TODO: router/schema
async def get_forms_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(engine) as session:
        statement = select(model.ZMSFormulator).join(model.ZMSSite). \
            where(model.ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/datatables", summary='Datatables', response_model=list[schema.ZMSDataTable])  # TODO: router/schema
async def get_datatables(
        offset: int = 0,
        limit: int = 100):
    with Session(engine) as session:
        statement = select(model.ZMSDataTable, model.ZMSSite).join(model.ZMSSite). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.ZMSDataTable.parse_obj({
                'datatablePath': res.ZMSDataTable.path,
                'datatableSite': get_subdomain(res.ZMSSite.domain),
                'datatableDomain': strip_cmstest(res.ZMSSite.domain),
                'datatableUrl': res.ZMSDataTable.dataurl.strip() != '' and res.ZMSDataTable.dataurl.strip() or None,
            }))
        return rtn
