from fastapi import APIRouter
from sqlmodel import Session, select, or_
from datetime import datetime

from ..db import engine
from ..models.newsevents import NewsEvents
from ..models.zmsobjects import ZMSSite
from ..schemas import newsevents as schema
from ..helpers import Lang, get_attr_by_lang, strip_cmstest, local_timezone

router = APIRouter(
    prefix="/v3",
    tags=["News and Events"])


@router.get("/news", response_model=list[schema.News])
async def get_news(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 50):

    rtn = []

    with Session(engine) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'news').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(or_(ZMSSite.type == 'Home',
                               ZMSSite.type == 'Fakultaet',
                               ZMSSite.type == 'Institut',
                               ZMSSite.type == 'Uniaktuell',  # to fetch UB (Library) by deprecated type
                               ZMSSite.type == 'Microsite')).
                     order_by(NewsEvents.level).
                     order_by(ZMSSite.type).  # TODO: introduce order_by(lastmod) for News...?!
                     offset(offset).limit(limit)]

        results = session.exec(statement[0])

        for res in results.all():
            rtn.append(schema.News.parse_obj({
                'newsDate': local_timezone(res.NewsEvents.start_dt),
                'newsTitle': get_attr_by_lang(lang,
                                              de=res.NewsEvents.title_de,
                                              en=res.NewsEvents.title_en,
                                              fr=res.NewsEvents.title_fr),
                'newsUrl': get_attr_by_lang(lang,
                                            de=res.NewsEvents.url_de,
                                            en=res.NewsEvents.url_en,
                                            fr=res.NewsEvents.url_fr),
                'newsInfos': get_attr_by_lang(lang,
                                              de=res.NewsEvents.infos_de,
                                              en=res.NewsEvents.infos_en,
                                              fr=res.NewsEvents.infos_fr),
                'newsTopics': get_attr_by_lang(lang,
                                               de=res.NewsEvents.topics_de,
                                               en=res.NewsEvents.topics_en,
                                               fr=res.NewsEvents.topics_fr),
                'newsImage': get_attr_by_lang(lang,
                                              de=res.NewsEvents.image_de,
                                              en=res.NewsEvents.image_en,
                                              fr=res.NewsEvents.image_fr),
                'sectionTitle': get_attr_by_lang(lang,
                                                 de=res.ZMSSite.title_de,
                                                 en=res.ZMSSite.title_en,
                                                 fr=res.ZMSSite.title_fr),
                'sectionDomain': f'https://{strip_cmstest(res.ZMSSite.domain)}',
                'sectionType': res.ZMSSite.type,
                'dataSource': res.NewsEvents.path,
                'dataLevel': res.NewsEvents.level,
                'dataUuid': res.NewsEvents.uuid,
            }))

    return rtn


@router.get("/events", response_model=list[schema.Event])
async def get_events(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 50):

    rtn = []

    with Session(engine) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'event').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(NewsEvents.end_dt > datetime.utcnow()).
                     where(or_(ZMSSite.type == 'Home',
                               ZMSSite.type == 'Fakultaet',
                               ZMSSite.type == 'Institut',
                               ZMSSite.type == 'Uniaktuell',  # to fetch UB (Library) by deprecated type
                               ZMSSite.type == 'Microsite')).
                     order_by(NewsEvents.start_dt).
                     order_by(ZMSSite.type).
                     offset(offset).limit(limit)]

        results = session.exec(statement[0])

        for res in results.all():
            section_domain = f'https://{strip_cmstest(res.ZMSSite.domain)}'
            section_type = res.ZMSSite.type
            data_source = res.NewsEvents.path
            data_level = res.NewsEvents.level
            data_uuid = res.NewsEvents.uuid

            if res.NewsEvents.path == 'agenda_portal':
                data_source = 'https://agenda.unibe.ch/agenda.json'
                section_type = 'Agenda'
                data_uuid = None
            elif res.NewsEvents.path == 'agenda_library':
                data_source = f'https://agenda.ub.unibe.ch/{lang}/api/event'
                section_type = 'Agenda'
                data_uuid = None

            rtn.append(schema.Event.parse_obj({
                'eventStart': local_timezone(res.NewsEvents.start_dt),
                'eventEnd': local_timezone(res.NewsEvents.end_dt),
                'eventTitle': get_attr_by_lang(lang,
                                               de=res.NewsEvents.title_de,
                                               en=res.NewsEvents.title_en,
                                               fr=res.NewsEvents.title_fr),
                'eventLocation': get_attr_by_lang(lang,
                                                  de=res.NewsEvents.location_de,
                                                  en=res.NewsEvents.location_en,
                                                  fr=res.NewsEvents.location_fr),
                'eventUrl': get_attr_by_lang(lang,
                                             de=res.NewsEvents.url_de,
                                             en=res.NewsEvents.url_en,
                                             fr=res.NewsEvents.url_fr),
                'eventInfos': get_attr_by_lang(lang,
                                               de=res.NewsEvents.infos_de,
                                               en=res.NewsEvents.infos_en,
                                               fr=res.NewsEvents.infos_fr),
                'eventTopics': get_attr_by_lang(lang,
                                                de=res.NewsEvents.topics_de,
                                                en=res.NewsEvents.topics_en,
                                                fr=res.NewsEvents.topics_fr),
                'eventImage': get_attr_by_lang(lang,
                                               de=res.NewsEvents.image_de,
                                               en=res.NewsEvents.image_en,
                                               fr=res.NewsEvents.image_fr),
                'sectionTitle': get_attr_by_lang(lang,
                                                 de=res.ZMSSite.title_de,
                                                 en=res.ZMSSite.title_en,
                                                 fr=res.ZMSSite.title_fr),
                'sectionDomain': section_domain,
                'sectionType': section_type,
                'dataSource': data_source,
                'dataLevel': data_level,
                'dataUuid': data_uuid,
            }))

    return rtn
