from fastapi import APIRouter
from sqlmodel import Session, select

from zms.unibe.datatables.sqlmodels.ZMSDataTable import ZMSDataTable
from zms.unibe.formulator.sqlmodels.ZMSFormulator import ZMSFormulator
from zms.unibe.foundation.sqlmodels.ZMSDocument import ZMSDocument
from zms.unibe.foundation.sqlmodels.ZMSFolder import ZMSFolder
from zms.unibe.foundation.sqlmodels.ZMSSite import ZMSSite
from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.zms2sql.attributes import Lang, get_attr_by_lang, strip_cmstest, get_subdomain
from ..schemas import zmsobjects as schema

router = APIRouter(
    prefix="/v1/zms",
    tags=["ZMS Objects"],
    include_in_schema=True
)


@router.get("/sites", summary='Content Sites', response_model=list[schema.ZMSSite])
async def get_content_sites(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 500):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSSite). \
            where(ZMSSite.domain != ''). \
            where(get_attr_by_lang(lang,
                                   de=ZMSSite.active_de,
                                   en=ZMSSite.active_en,
                                   fr=ZMSSite.active_fr)). \
            order_by(ZMSSite.domain). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            rtn.append(schema.ZMSSite.model_validate({
                'siteUuid': res.uuid,
                'sitePath': res.path,
                'siteType': res.type,
                'siteShort': get_subdomain(res.domain),
                'siteTitle': get_attr_by_lang(lang, de=res.title_de, en=res.title_en, fr=res.title_fr),
                'siteAlias': ', '.join(strip_cmstest(res.alias).strip().split()),
                'siteDomain': strip_cmstest(res.domain),
                'siteParentUuid': res.parent_uuid,
            }))
        return rtn


@router.get("/documents/{site}", response_model=list[ZMSDocument])  # TODO: router/schema
async def get_documents_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSDocument).join(ZMSSite). \
            where(ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/folders/{site}", response_model=list[ZMSFolder])  # TODO: router/schema
async def get_folders_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSFolder).join(ZMSSite). \
            where(ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/forms/{site}", summary='Forms by Site', response_model=list[ZMSFormulator])  # TODO: router/schema
async def get_forms_by_site(
        site: str,
        offset: int = 0,
        limit: int = 10):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSFormulator).join(ZMSSite). \
            where(ZMSSite.domain == get_subdomain(site, reverse=True)). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        return results.all()


@router.get("/datatables", summary='Datatables', response_model=list[schema.ZMSDataTable])  # TODO: router/schema
async def get_datatables(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 100):
    with Session(connect_sqldb()) as session:
        statement = select(ZMSDataTable, ZMSSite).join(ZMSSite). \
            offset(offset).limit(limit)
        results = session.exec(statement)
        rtn = []
        for res in results.all():
            data_url = get_attr_by_lang(lang,
                                        de=res.ZMSDataTable.dataurl_de, 
                                        en=res.ZMSDataTable.dataurl_en,
                                        fr=res.ZMSDataTable.dataurl_fr).strip()
            rtn.append(schema.ZMSDataTable.model_validate({
                'datatablePath': res.ZMSDataTable.path,
                'datatableSite': get_subdomain(res.ZMSSite.domain),
                'datatableDomain': strip_cmstest(res.ZMSSite.domain),
                'datatableUrl': data_url if data_url != '' else None,
            }))
        return rtn
