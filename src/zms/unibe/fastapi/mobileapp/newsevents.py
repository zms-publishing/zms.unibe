from datetime import datetime, timedelta, timezone
from uuid import UUID

from anytree import Node, RenderTree
from anytree.exporter import DictExporter, JsonExporter
from devtools import debug
from fastapi import APIRouter, Query
from sqlmodel import Session, not_, or_, select

from zms.unibe.agenda.sqlmodels.StatusMessages import StatusMessage
from zms.unibe.fastapi.meta import Tags
from zms.unibe.foundation.sqlmodels.ZMSSite import ZMSSite
from zms.unibe.mobileapp.schemas import NewsEventsSchema as schema
from zms.unibe.mobileapp.sqlmodels.NewsEvents import NewsEvents
from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.enums import Locale, SiteType
from zms.unibe.utils.helpers import get_attr_by_lang, local_timezone, strip_cmstest

router = APIRouter(tags=[Tags.mobile])


@router.get("/news", summary="News", response_model=schema.NewsResponse,
            description='News from portal at <a href="https://www.unibe.ch" target="_blank">unibe.ch</a> '
                        'and faculties at <a href="https://www.unibe.ch/fakultaeteninstitute" '
                        'target="_blank">unibe.ch/fakultaeteninstitute</a>')
async def get_news(
        lang: Locale = Locale.de,
        sections: list[UUID] | None = Query(None, description='Filter by sections'),
        date_after: datetime | None = Query(None, description='Filter by date after (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(connect_sqldb()) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'news').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(date_after is None and True or (NewsEvents.lastmod_dt_de > date_after)).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/uniaktuell'))).
                     where(not_(ZMSSite.path.contains('/uni_aktuell'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     where(not_(NewsEvents.path.contains('/trashcan'))).
                     where(or_(sections is None and True or (NewsEvents.site_uuid == section for section in sections))).
                     order_by(NewsEvents.level).
                     order_by(NewsEvents.sort_id_parent).
                     order_by(NewsEvents.sort_id).
                     order_by(ZMSSite.type)]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            section = schema.Section(
                type=res.ZMSSite.type,
                title=get_attr_by_lang(lang,
                                       de=res.ZMSSite.title_de,
                                       en=res.ZMSSite.title_en,
                                       fr=res.ZMSSite.title_fr),
                domain=f'https://{strip_cmstest(res.ZMSSite.domain)}',
                path=res.ZMSSite.path,
                uuid=res.ZMSSite.uuid
            )

            data.append(schema.News.model_validate({
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
                'dataSort': res.NewsEvents.sort_id,
                'dataSortParent': res.NewsEvents.sort_id_parent,
                'dataUuid': res.NewsEvents.uuid,
            }))

        return {
            'offset': offset,
            'limit': limit,
            'total': len(total.all()),
            'data': data
        }


def fetch_events(lang, sections, start_after, end_before, offset, limit):

    with Session(connect_sqldb()) as session:

        statement = [select(NewsEvents, ZMSSite).join(ZMSSite).
                     where(NewsEvents.type == 'event').
                     where(get_attr_by_lang(lang,
                                            de=NewsEvents.active_de,
                                            en=NewsEvents.active_en,
                                            fr=NewsEvents.active_fr)).
                     where(start_after is None and True or (NewsEvents.start_dt > start_after)).
                     where(end_before is None and True or (NewsEvents.end_dt < end_before)).
                     where(NewsEvents.end_dt > datetime.now(timezone.utc)).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/uniaktuell'))).
                     where(not_(ZMSSite.path.contains('/uni_aktuell'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     where(not_(NewsEvents.path.contains('/trashcan'))).
                     where(or_(sections is None and True or (NewsEvents.site_uuid == section for section in sections))).
                     order_by(NewsEvents.start_dt).
                     order_by(ZMSSite.type)]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        return results.all(), total.all()


def get_sections_tree(data, lang):

    root = Node(UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2'),
                title='UniBE',
                path='/unibe/content',
                uuid=UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2'))
    nodes = {}

    # set nodes with parent == root
    for i, obj in enumerate(data):
        if obj.parent_uuid == UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2') and \
                obj.uuid != UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            nodes[obj.uuid] = Node(obj.uuid, parent=root,
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)

    # set nodes with parent != root
    for i, obj in enumerate(data):
        if obj.parent_uuid != UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2') and \
                obj.uuid != UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            nodes[obj.uuid] = Node(obj.uuid,
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)

    # set parent nodes - Prerequisite: order_by(ZMSSite.level) to process in hierarchy
    for i, obj in enumerate(data):
        if obj.parent_uuid in nodes.keys():
            nodes[obj.uuid] = Node(obj.uuid, parent=nodes[obj.parent_uuid],
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)
        elif obj.parent_uuid != UUID('urn:uuid:2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            debug(obj.parent_uuid, obj.uuid)

    for pre, fill, node in RenderTree(root):
        # print("%s%s" % (pre, node.title))
        pass

    jsonexporter = JsonExporter(indent=2, sort_keys=True, ensure_ascii=False)
    # print(jsonexporter.export(root))

    dictexporter = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k != "name"])

    return dictexporter.export(root)


@router.get("/events", summary='Events', response_model=schema.EventResponse,
            description='Events from portal at <a href="https://www.unibe.ch" target="_blank">unibe.ch</a> '
                        'and faculties at <a href="https://www.unibe.ch/fakultaeteninstitute" '
                        'target="_blank">unibe.ch/fakultaeteninstitute</a> as well as '
                        '<a href="https://agenda.unibe.ch" target="_blank">agenda.unibe.ch</a> and '
                        '<a href="https://agenda.ub.unibe.ch" target="_blank">agenda.ub.unibe.ch</a>')
async def get_events(
        lang: Locale = Locale.de,
        sections: list[UUID] | None = Query(None, description='Filter by sections'),
        start_after: datetime | None = Query(None, description='Filter by start after (UTC)'),
        end_before: datetime | None = Query(None, description='Filter by end before (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []
    results, total = fetch_events(lang, sections, start_after, end_before, offset, limit)

    for res in results:
        section = schema.Section(
            type=res.ZMSSite.type,
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

        data.append(schema.Event.model_validate({
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
        'total': len(total),
        'data': data
    }


@router.get("/sections", summary='Sections to filter News and Events')
async def get_sections(
        lang: Locale = Locale.de,
        tree: bool = False,
        types: list[SiteType] = Query([SiteType.Fakultaet.value,
                                       SiteType.Departement.value,
                                       SiteType.Institut.value,
                                       SiteType.Library.value,
                                       SiteType.Unisport.value]),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(connect_sqldb()) as session:

        statement = [select(NewsEvents.site_uuid, ZMSSite).join(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=ZMSSite.active_de,
                                            en=ZMSSite.active_en,
                                            fr=ZMSSite.active_fr)).
                     where(ZMSSite.type.in_(types + ['', 'Home'])).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/uniaktuell'))).
                     where(not_(ZMSSite.path.contains('/uni_aktuell'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     group_by(NewsEvents.site_uuid,
                              ZMSSite.title_de,
                              ZMSSite.title_en,
                              ZMSSite.title_fr,
                              ZMSSite.domain,
                              ZMSSite.type,
                              ZMSSite.uuid).
                     order_by(get_attr_by_lang(lang,
                                               de=ZMSSite.title_de,
                                               en=ZMSSite.title_en,
                                               fr=ZMSSite.title_fr)),
                     select(ZMSSite).
                     where(get_attr_by_lang(lang,
                                            de=ZMSSite.active_de,
                                            en=ZMSSite.active_en,
                                            fr=ZMSSite.active_fr)).
                     where(get_attr_by_lang(lang,
                                            de=ZMSSite.title_de,
                                            en=ZMSSite.title_en,
                                            fr=ZMSSite.title_fr) != '').
                     where(ZMSSite.type.in_(types + ['', 'Home'])).
                     where(not_(ZMSSite.path.contains('/arbeitgeberin'))).
                     where(not_(ZMSSite.path.contains('/images'))).
                     where(not_(ZMSSite.path.contains('/jahresberichte'))).
                     where(not_(ZMSSite.path.contains('/uniapp'))).
                     where(not_(ZMSSite.path.contains('/uniintern'))).
                     where(not_(ZMSSite.path.contains('/uniaktuell'))).
                     where(not_(ZMSSite.path.contains('/uni_aktuell'))).
                     where(not_(ZMSSite.path.contains('/zms_schulung'))).
                     order_by(ZMSSite.level).
                     order_by(get_attr_by_lang(lang,
                                               de=ZMSSite.title_de,
                                               en=ZMSSite.title_en,
                                               fr=ZMSSite.title_fr))]

        if tree:
            results = session.exec(statement[1])
            return get_sections_tree(results.all(), lang)

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            data.append(schema.Section.model_validate({
                'title': get_attr_by_lang(lang,
                                          de=res.ZMSSite.title_de,
                                          en=res.ZMSSite.title_en,
                                          fr=res.ZMSSite.title_fr),
                'domain': strip_cmstest(res.ZMSSite.domain),
                'type': res.ZMSSite.type,
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
                        '<a href="https://id.unibe.ch/statusmeldungen" target="_blank">id.unibe.ch/statusmeldungen</a>')
async def get_statusmessages(
        start_after: datetime | None = Query(None, description='Filter by start after (UTC)'),
        end_before: datetime | None = Query(None, description='Filter by end before (UTC)'),
        offset: int = 0,
        limit: int = 20):

    data = []

    with Session(connect_sqldb()) as session:

        statement = [select(StatusMessage).
                     where(start_after is None and True or (StatusMessage.begin > start_after)).
                     where(end_before is None and True or (StatusMessage.end < end_before)).
                     where(or_(StatusMessage.end > datetime.now(timezone.utc) - timedelta(days=1),  # show resolved by yesterday
                               StatusMessage.end == datetime.fromisoformat('1970-01-01T00:00:00'))).  # show open issues
                     order_by(StatusMessage.begin).
                     order_by(StatusMessage.end.desc())]

        results = session.exec(statement[0].offset(offset).limit(limit))
        total = session.exec(statement[0])

        for res in results.all():
            section = schema.Section(
                type=res.type,
                title='IT Services',
                domain='https://id.unibe.ch/statusmeldungen',
                path=None,
                uuid=None
            )
            data.append(schema.StatusMessage.model_validate({
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
