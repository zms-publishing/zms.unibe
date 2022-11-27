from fastapi import APIRouter, Query
from sqlmodel import Session, select, or_
from datetime import datetime, timedelta
from uuid import UUID

from ..db import engine
from ..models.newsevents import NewsEvents, StatusMessage
from ..models.zmsobjects import ZMSSite
from ..schemas import newsevents as schema
from ..helpers import Lang, get_attr_by_lang, strip_cmstest, local_timezone

router = APIRouter(
    prefix="/v3",
    tags=["UniBE News and Events"])


@router.get("/news", summary="News", response_model=schema.NewsResponse,
            description='News from portal at <a href="https://www.unibe.ch" target="_blank">unibe.ch</a> '
                        'and faculties at <a href="https://www.unibe.ch/fakultaeteninstitute" '
                        'target="_blank">unibe.ch/fakultaeteninstitute</a>')
async def get_news(
        lang: Lang = Lang.de,
        sections: list[UUID] | None = Query(None, description='Filter by sections'),
        date: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'news').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(date is None and True or (NewsEvents.lastmod_dt_de > date)).
                     where(or_(ZMSSite.type == 'Home',
                               ZMSSite.type == 'Fakultaet',
                               ZMSSite.type == 'Institut',
                               ZMSSite.type == 'Uniaktuell',  # to fetch UB (Library) by deprecated type
                               ZMSSite.type == 'Microsite')).
                     where(or_(sections is None and True or (NewsEvents.site_uuid == section for section in sections))).
                     # order_by(NewsEvents.level).
                     order_by(get_attr_by_lang(lang,
                                               de=NewsEvents.lastmod_dt_de,
                                               en=NewsEvents.lastmod_dt_en,
                                               fr=NewsEvents.lastmod_dt_fr).desc()).
                     order_by(ZMSSite.type)]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            if '/uniintern' in res.ZMSSite.path \
                    or '/zms_schulung' in res.ZMSSite.path \
                    or '/trashcan' in res.NewsEvents.path:
                continue

            section = schema.Section(
                type='/unibiblio' in res.ZMSSite.path and
                     'Library' or res.ZMSSite.type,  # overwrite deprecated type "Uniaktuell" of UB (Library)
                title=get_attr_by_lang(lang,
                                       de=res.ZMSSite.title_de,
                                       en=res.ZMSSite.title_en,
                                       fr=res.ZMSSite.title_fr),
                domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
                path=res.ZMSSite.path,
                uuid=res.ZMSSite.uuid
            )

            data.append(schema.News.parse_obj({
                'date': local_timezone(get_attr_by_lang(lang,
                                                        de=res.NewsEvents.lastmod_dt_de,
                                                        en=res.NewsEvents.lastmod_dt_en,
                                                        fr=res.NewsEvents.lastmod_dt_fr)),
                'title': get_attr_by_lang(lang,
                                          de=res.NewsEvents.title_de,
                                          en=res.NewsEvents.title_en,
                                          fr=res.NewsEvents.title_fr),
                'url': get_attr_by_lang(lang,
                                        de=res.NewsEvents.url_de,
                                        en=res.NewsEvents.url_en,
                                        fr=res.NewsEvents.url_fr),
                'infos': get_attr_by_lang(lang,
                                          de=res.NewsEvents.infos_de,
                                          en=res.NewsEvents.infos_en,
                                          fr=res.NewsEvents.infos_fr),
                'topics': get_attr_by_lang(lang,
                                           de=res.NewsEvents.topics_de,
                                           en=res.NewsEvents.topics_en,
                                           fr=res.NewsEvents.topics_fr),
                'image': get_attr_by_lang(lang,
                                          de=res.NewsEvents.image_de,
                                          en=res.NewsEvents.image_en,
                                          fr=res.NewsEvents.image_fr),
                'section': section,
                'dataSource': res.NewsEvents.path,
                'dataLevel': res.NewsEvents.level,
                'dataUuid': res.NewsEvents.uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }


@router.get("/events", summary='Events', response_model=schema.EventResponse,
            description='Events from portal at <a href="https://www.unibe.ch" target="_blank">unibe.ch</a> '
                        'and faculties at <a href="https://www.unibe.ch/fakultaeteninstitute" '
                        'target="_blank">unibe.ch/fakultaeteninstitute</a> as well as '
                        '<a href="https://agenda.unibe.ch" target="_blank">agenda.unibe.ch</a> and '
                        '<a href="https://agenda.ub.unibe.ch" target="_blank">agenda.ub.unibe.ch</a>')
async def get_events(
        lang: Lang = Lang.de,
        sections: list[UUID] | None = Query(None, description='Filter by sections'),
        start: datetime | None = Query(None, description='Filter by start after (UTC)'),
        end: datetime | None = Query(None, description='Filter by end before (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'event').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(start is None and True or (NewsEvents.start_dt > start)).
                     where(end is None and True or (NewsEvents.end_dt < end)).
                     where(NewsEvents.end_dt > datetime.utcnow()).
                     where(or_(ZMSSite.type == 'Home',
                               ZMSSite.type == 'Fakultaet',
                               ZMSSite.type == 'Institut',
                               ZMSSite.type == 'Uniaktuell',  # to fetch UB (Library) by deprecated type
                               ZMSSite.type == 'Microsite')).
                     where(or_(sections is None and True or (NewsEvents.site_uuid == section for section in sections))).
                     order_by(NewsEvents.start_dt).
                     order_by(ZMSSite.type)]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            if '/uniintern' in res.ZMSSite.path \
                    or '/zms_schulung' in res.ZMSSite.path \
                    or '/trashcan' in res.NewsEvents.path:
                continue

            section = schema.Section(
                type='/unibiblio' in res.ZMSSite.path and
                     'Library' or res.ZMSSite.type,  # overwrite deprecated type "Uniaktuell" of UB (Library)
                title=get_attr_by_lang(lang,
                                       de=res.ZMSSite.title_de,
                                       en=res.ZMSSite.title_en,
                                       fr=res.ZMSSite.title_fr),
                domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
                path=res.ZMSSite.path,
                uuid=res.ZMSSite.uuid
            )

            data_source = res.NewsEvents.path
            data_level = res.NewsEvents.level
            data_uuid = res.NewsEvents.uuid

            if res.NewsEvents.path == 'agenda_portal':
                data_source = 'https://agenda.unibe.ch/agenda.json'
                section.type = 'Agenda Portal'
                data_uuid = None
            elif res.NewsEvents.path == 'agenda_library':
                data_source = f'https://agenda.ub.unibe.ch/{lang}/api/event'
                section.type = 'Agenda Library'
                data_uuid = None

            data.append(schema.Event.parse_obj({
                'start': local_timezone(res.NewsEvents.start_dt),
                'end': local_timezone(res.NewsEvents.end_dt),
                'title': get_attr_by_lang(lang,
                                          de=res.NewsEvents.title_de,
                                          en=res.NewsEvents.title_en,
                                          fr=res.NewsEvents.title_fr),
                'location': get_attr_by_lang(lang,
                                             de=res.NewsEvents.location_de,
                                             en=res.NewsEvents.location_en,
                                             fr=res.NewsEvents.location_fr),
                'url': get_attr_by_lang(lang,
                                        de=res.NewsEvents.url_de,
                                        en=res.NewsEvents.url_en,
                                        fr=res.NewsEvents.url_fr),
                'infos': get_attr_by_lang(lang,
                                          de=res.NewsEvents.infos_de,
                                          en=res.NewsEvents.infos_en,
                                          fr=res.NewsEvents.infos_fr),
                'topics': get_attr_by_lang(lang,
                                           de=res.NewsEvents.topics_de,
                                           en=res.NewsEvents.topics_en,
                                           fr=res.NewsEvents.topics_fr),
                'image': get_attr_by_lang(lang,
                                          de=res.NewsEvents.image_de,
                                          en=res.NewsEvents.image_en,
                                          fr=res.NewsEvents.image_fr),
                'section': section,
                'dataSource': data_source,
                'dataLevel': data_level,
                'dataUuid': data_uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }


@router.get("/sections", summary='Sections to filter News and Events', response_model=schema.SectionResponse)
async def get_sections(
        lang: Lang = Lang.de,
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:

        statement = [select(NewsEvents.site_uuid, ZMSSite).join(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=ZMSSite.active_de,
                                            en=ZMSSite.active_en,
                                            fr=ZMSSite.active_fr)).
                     group_by(NewsEvents.site_uuid,
                              ZMSSite.title_de,
                              ZMSSite.title_en,
                              ZMSSite.title_fr,
                              ZMSSite.domain,
                              ZMSSite.type,
                              ZMSSite.uuid).
                     order_by(ZMSSite.type.desc()).
                     order_by(get_attr_by_lang(lang,
                                               de=ZMSSite.title_de,
                                               en=ZMSSite.title_en,
                                               fr=ZMSSite.title_fr))]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            if '/uniintern' in res.ZMSSite.path \
                    or '/zms_schulung' in res.ZMSSite.path:
                continue
            data.append(schema.Section.parse_obj({
                'title': get_attr_by_lang(lang,
                                          de=res.ZMSSite.title_de,
                                          en=res.ZMSSite.title_en,
                                          fr=res.ZMSSite.title_fr),
                'domain': strip_cmstest(res.ZMSSite.domain),
                'type': '/unibiblio' in res.ZMSSite.path and
                        'Library' or res.ZMSSite.type,  # overwrite deprecated type "Uniaktuell" of UB (Library)
                'path': res.ZMSSite.path,
                'uuid': res.ZMSSite.uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }


@router.get("/statusmessages", summary='IT Status messages', response_model=schema.StatusMessageResponse,
            description='IT Status messages from '
                        '<a href="http://id.unibe.ch/statusmeldungen" target="_blank">id.unibe.ch/statusmeldungen</a>')
async def get_statusmessages(
        start: datetime | None = Query(None, description='Filter by start after (UTC)'),
        end: datetime | None = Query(None, description='Filter by end before (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(engine) as session:

        statement = [select(StatusMessage).
                     where(start is None and True or (StatusMessage.begin > start)).
                     where(end is None and True or (StatusMessage.end < end)).
                     where(or_(StatusMessage.end > datetime.utcnow() - timedelta(days=1),  # show resolved by yesterday
                               StatusMessage.end == datetime.fromisoformat('1970-01-01T00:00:00'))).  # show open issues
                     order_by(StatusMessage.begin).
                     order_by(StatusMessage.end.desc())]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            section = schema.Section(
                type=res.type,
                title='IT Services',
                domain='http://id.unibe.ch/statusmeldungen',
                path=None,
                uuid=None
            )
            data.append(schema.StatusMessage.parse_obj({
                'title': res.subject,
                'start': local_timezone(res.begin),
                'end': res.end > local_timezone(datetime.fromisoformat('1970-01-01T00:00:00+00:00'))
                       and local_timezone(res.end) or None,
                'infos': f'{res.description}\n\n{res.info}',
                'topics': res.service,
                'section': section,
                'dataSource': 'https://api.epc.unibe.ch/announcements/api/ServiceAnnouncements',
                'dataLevel': 1,
                'dataUuid': None
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }
