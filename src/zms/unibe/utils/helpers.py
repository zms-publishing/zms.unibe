import io
import time
from datetime import datetime
from uuid import UUID

import pytz
from Products.zms import standard
from anytree import Node, RenderTree
from anytree.exporter import JsonExporter, DictExporter
from devtools import debug
from ics import Calendar, Event

from .zms2sql.attributes import get_attr_by_lang, strip_cmstest


def local_timezone(dt=None):
    if dt is None:
        dt = datetime.now()
    if isinstance(dt, time.struct_time):
        dt = standard.format_datetime_iso(dt)
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.astimezone(pytz.timezone('Europe/Zurich'))


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


def generate_ics(lang, results):

    calendar = Calendar()

    for res in results:
        event = Event()
        event.name = get_attr_by_lang(lang,
                                      de=res.NewsEvents.title_de,
                                      en=res.NewsEvents.title_en,
                                      fr=res.NewsEvents.title_fr)
        event.begin = local_timezone(res.NewsEvents.start_dt)
        event.end = local_timezone(res.NewsEvents.end_dt)
        event.description = get_attr_by_lang(lang,
                                             de=res.NewsEvents.infos_de,
                                             en=res.NewsEvents.infos_en,
                                             fr=res.NewsEvents.infos_fr)
        event.location = get_attr_by_lang(lang,
                                          de=res.NewsEvents.location_de,
                                          en=res.NewsEvents.location_en,
                                          fr=res.NewsEvents.location_fr)
        event.url = get_attr_by_lang(lang,
                                     de=res.NewsEvents.url_de,
                                     en=res.NewsEvents.url_en,
                                     fr=res.NewsEvents.url_fr)
        calendar.events.add(event)

    return io.StringIO(calendar.serialize())
