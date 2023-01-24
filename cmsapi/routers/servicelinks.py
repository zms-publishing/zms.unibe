from fastapi import APIRouter
from sqlmodel import Session, select
from uuid import UUID

from ..db import engine
from ..schemas import servicelinks as schema
from ..helpers import Lang, local_timezone, get_attr_by_lang

from ..models.servicelinks import ServiceLink

router = APIRouter(
    prefix="/v3/app",
    tags=["UniBE Mobile App Service Links"]
)


def _retrieve_service_links(lang, uuid):

    data = []

    if uuid == UUID('1c0a8927-bfb4-4215-a8fd-c41bba079d21'):  # handle files if location
        service_filter = ServiceLink.meta_id == 'ZMSFile'
    else:
        service_filter = ServiceLink.parent_uuid == uuid

    with Session(engine) as session:
        statement = [select(ServiceLink).
                     where(get_attr_by_lang(lang,
                                            de=ServiceLink.active_de,
                                            en=ServiceLink.active_en,
                                            fr=ServiceLink.active_fr)).
                     where(service_filter).
                     where(ServiceLink.meta_id != 'ZMSNote').
                     where(ServiceLink.meta_id != 'codeblock').
                     order_by(get_attr_by_lang(lang,
                                               de=ServiceLink.title_de,
                                               en=ServiceLink.title_en,
                                               fr=ServiceLink.title_fr))]

        results = session.exec(statement[0])

        for res in results.all():
            service_title = get_attr_by_lang(lang,
                                             de=res.title_de,
                                             en=res.title_en,
                                             fr=res.title_fr).strip()
            service_name = get_attr_by_lang(lang,
                                            de=res.parent_title_de,
                                            en=res.parent_title_en,
                                            fr=res.parent_title_fr).strip()
            service_title = service_title != '' and service_title or service_name

            service_href = get_attr_by_lang(lang,
                                            de=res.href_de,
                                            en=res.href_en,
                                            fr=res.href_fr).strip()
            service_url = get_attr_by_lang(lang,
                                           de=res.url_de,
                                           en=res.url_en,
                                           fr=res.url_fr).strip()
            service_link = service_href != '' and service_href or service_url

            service_info = get_attr_by_lang(lang,
                                            de=res.text_de,
                                            en=res.text_en,
                                            fr=res.text_fr).strip()
            service_keywords = get_attr_by_lang(lang,
                                                de=res.keywords_de,
                                                en=res.keywords_en,
                                                fr=res.keywords_fr).strip()
            service_info = service_info != '' and service_info or service_keywords

            if uuid == UUID('1c0a8927-bfb4-4215-a8fd-c41bba079d21'):  # map attributes if location
                service_info = get_attr_by_lang(lang,
                                                de=res.parent_title_de,
                                                en=res.parent_title_en,
                                                fr=res.parent_title_fr).strip()

            data.append(schema.ServiceLink.parse_obj({
                'title': service_title,
                'url': service_link,
                'info': service_info,
                'path': res.path,
                'uuid': res.uuid,
                'lastmod': get_attr_by_lang(lang,
                                            de=local_timezone(res.lastmod_dt_de),
                                            en=local_timezone(res.lastmod_dt_en),
                                            fr=local_timezone(res.lastmod_dt_fr)),
            }))

    return data


@router.get("/contact", summary='Contact', response_model=list[schema.ServiceLink])
async def get_app_contact(
        lang: Lang = Lang.de):
    return _retrieve_service_links(lang, UUID('58115e60-e80b-44c1-9a7d-bc65a42c9d5a'))


@router.get("/imprint", summary='Imprint', response_model=list[schema.ServiceLink])
async def get_app_imprint(
        lang: Lang = Lang.de):
    return _retrieve_service_links(lang, UUID('d15e37f5-b317-4b47-baf1-c203a34bd0ad'))


@router.get("/indexaz", summary='Index A-Z', response_model=list[schema.ServiceLink])
async def get_app_indexaz(
        lang: Lang = Lang.de):
    return _retrieve_service_links(lang, UUID('27bfdd98-c79b-4dd4-b69a-dd1bde958d0b'))


@router.get("/locations", summary='Locations', response_model=list[schema.ServiceLink])
async def get_app_locations(
        lang: Lang = Lang.de):
    return _retrieve_service_links(Lang.de, UUID('1c0a8927-bfb4-4215-a8fd-c41bba079d21'))


@router.get("/privacypolicy", summary='Privacy Policy', response_model=list[schema.ServiceLink])
async def get_app_privacypolicy(
        lang: Lang = Lang.de):
    return _retrieve_service_links(lang, UUID('a7f29281-43e0-4607-871b-39e66204bb31'))


@router.get("/termsofservice", summary='Terms of Service', response_model=list[schema.ServiceLink])
async def get_app_termsofservice(
        lang: Lang = Lang.de):
    return _retrieve_service_links(lang, UUID('4b570198-0485-4f75-8242-9e5a7528351a'))
