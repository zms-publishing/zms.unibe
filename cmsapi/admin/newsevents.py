from sqlmodel import select, or_, inspect
from uuid import UUID, uuid4
from datetime import datetime

from ..models.newsevents import NewsEvents
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.teaserelement2022 import TeaserElement2022
from ..models.newsbox import Newsbox


def _store_newsevents_data(session, sqlengine):  # fill intermediate table consolidating data sources for queries

    if inspect(sqlengine).has_table(NewsEvents.__table__):
        NewsEvents.__table__.drop(sqlengine)
    NewsEvents.__table__.create(sqlengine)

    # DATA SOURCE 1 ######################
    statement = select(AgendaPortal)  # DE
    results = session.exec(statement)
    for res in results.all():
        obj = NewsEvents()
        obj.uuid = uuid4()  # temporary UUID until next import - for internal use only
        obj.site_uuid = UUID('9c92af4f-6e95-4391-86d5-76eb8ad48360')  # UniBE Portal
        obj.active_de = True
        obj.active_en = False
        obj.active_fr = False

        obj.title_de = res.veranstaltung_titel
        obj.type = 'event'
        obj.path = 'agenda_portal'
        obj.level = 1
        obj.start_dt = res.json_datum_zeit_start
        obj.end_dt = res.json_datum_zeit_end > res.json_datum_zeit_start and \
                     res.json_datum_zeit_end or \
                     res.json_datum_zeit_start  # to filter out outdated Events - see where(NewsEvents.end_dt > datetime.utcnow())
        obj.location_de = f'{res.veranstaltung_horsaal}\n' \
                          f'{res.veranstaltung_gebaude_adresse}\n' \
                          f'{res.veranstaltung_ort}'

        obj.url_de = res.veranstalter_info_link
        obj.infos_de = res.veranstaltung_referenten
        obj.topics_de = res.veranstaltung_zyklus

        session.add(obj)
    session.commit()

    # DATA SOURCE 2 ######################
    statement = select(AgendaPortal)  # EN (as copy of DE to show content without a multilang AgendaPortal)
    results = session.exec(statement)
    for res in results.all():
        obj = NewsEvents()
        obj.uuid = uuid4()  # temporary UUID until next import - for internal use only
        obj.site_uuid = UUID('9c92af4f-6e95-4391-86d5-76eb8ad48360')  # UniBE Portal
        obj.active_de = False
        obj.active_en = True
        obj.active_fr = False

        obj.title_en = res.veranstaltung_titel
        obj.type = 'event'
        obj.path = 'agenda_portal'
        obj.level = 1
        obj.start_dt = res.json_datum_zeit_start
        obj.end_dt = res.json_datum_zeit_end > res.json_datum_zeit_start and \
                     res.json_datum_zeit_end or \
                     res.json_datum_zeit_start  # to filter out outdated Events - see where(NewsEvents.end_dt > datetime.utcnow())
        obj.location_en = f'{res.veranstaltung_horsaal}\n' \
                          f'{res.veranstaltung_gebaude_adresse}\n' \
                          f'{res.veranstaltung_ort}'

        obj.url_en = res.veranstalter_info_link
        obj.infos_en = res.veranstaltung_referenten
        obj.topics_en = res.veranstaltung_zyklus

        session.add(obj)
    session.commit()

    # DATA SOURCE 3 ###################
    statement = select(AgendaLibraryDE)
    results = session.exec(statement)
    for res in results.all():
        obj = NewsEvents()
        obj.uuid = uuid4()  # temporary UUID until next import - for internal use only
        obj.site_uuid = UUID('6f2a0c71-67cf-40db-bc36-8483471b1c32')  # UniBE Library
        obj.active_de = True
        obj.active_en = False
        obj.active_fr = False

        obj.title_de = res.title
        obj.type = 'event'
        obj.path = 'agenda_library'
        obj.level = 1
        obj.start_dt = res.startsAt
        obj.end_dt = res.endsAt > res.startsAt and \
                     res.endsAt or \
                     res.startsAt
        obj.location_de = res.venue

        obj.url_de = res.url
        obj.infos_de = ', '.join(res.subjects)
        obj.topics_de = res.eventType

        session.add(obj)
    session.commit()

    # DATA SOURCE 4 ###################
    statement = select(AgendaLibraryEN)
    results = session.exec(statement)
    for res in results.all():
        obj = NewsEvents()
        obj.uuid = uuid4()  # temporary UUID until next import - for internal use only
        obj.site_uuid = UUID('6f2a0c71-67cf-40db-bc36-8483471b1c32')  # UniBE Library
        obj.active_de = False
        obj.active_en = True
        obj.active_fr = False

        obj.title_en = res.title
        obj.type = 'event'
        obj.path = 'agenda_library'
        obj.level = 1
        obj.start_dt = res.startsAt
        obj.end_dt = res.endsAt > res.startsAt and \
                     res.endsAt or \
                     res.startsAt  # to filter out outdated Events - see where(NewsEvents.end_dt > datetime.utcnow())
        obj.location_en = res.venue

        obj.url_en = res.url
        obj.infos_en = ', '.join(res.subjects)
        obj.topics_en = res.eventType

        session.add(obj)
    session.commit()

    # DATA SOURCE 5 ######################
    statement = [select(TeaserElement2022).
                 where(or_(TeaserElement2022.active_de, TeaserElement2022.active_en, TeaserElement2022.active_fr)).
                 where(or_(TeaserElement2022.active_start_de <= datetime.utcnow(),
                           TeaserElement2022.active_start_en <= datetime.utcnow(),
                           TeaserElement2022.active_start_fr <= datetime.utcnow())).
                 where(or_(TeaserElement2022.active_end_de <= datetime.utcnow(),
                           TeaserElement2022.active_end_en <= datetime.utcnow(),
                           TeaserElement2022.active_end_fr <= datetime.utcnow()))]

    results = session.exec(statement[0])

    for res in results.all():

        if res.title_de == '&nbsp;' or res.title_en == '&nbsp;' or res.title_fr == '&nbsp;':
            continue

        if res.level == 2 and res.site_uuid == UUID('9c92af4f-6e95-4391-86d5-76eb8ad48360'):
            obj_level = 1  # rate UniBE Portal News higher - see order_by(NewsEvents.level) in routers/newsevents
        else:
            obj_level = res.level  # must always be >=2, because TeaserElement2022 are always be placed in a container

        obj = NewsEvents()
        obj.uuid = res.uuid
        obj.site_uuid = res.site_uuid
        obj.active_de = res.active_de
        obj.active_en = res.active_en
        obj.active_fr = res.active_fr
        obj.lastmod_dt_de = res.lastmod_dt_de
        obj.lastmod_dt_en = res.lastmod_dt_en
        obj.lastmod_dt_fr = res.lastmod_dt_fr

        obj.title_de = res.title_de
        obj.title_en = res.title_en
        obj.title_fr = res.title_fr
        obj.type = res.type
        obj.path = res.path
        obj.level = obj_level
        obj.start_dt = res.start_dt
        obj.end_dt = res.end_dt > res.start_dt and \
                     res.end_dt or \
                     res.start_dt  # to filter out outdated Events - see where(NewsEvents.end_dt > datetime.utcnow())
        obj.location_de = res.location
        obj.location_en = res.location
        obj.location_fr = res.location

        obj.url_de = res.url_de
        obj.url_en = res.url_en
        obj.url_fr = res.url_fr
        obj.infos_de = f'{res.text_de}\n\n{res.source_de}'
        obj.infos_en = f'{res.text_en}\n\n{res.source_en}'
        obj.infos_fr = f'{res.text_fr}\n\n{res.source_fr}'
        obj.topics_de = res.topic_de
        obj.topics_en = res.topic_en
        obj.topics_fr = res.topic_fr
        obj.image_de = res.img_de
        obj.image_en = res.img_en
        obj.image_fr = res.img_fr

        session.add(obj)
    session.commit()

    # DATA SOURCE 6 ######################
    statement = [select(Newsbox).
                 where(or_(Newsbox.active_de, Newsbox.active_en, Newsbox.active_fr)).
                 where(or_(Newsbox.active_start_de <= datetime.utcnow(),
                           Newsbox.active_start_en <= datetime.utcnow(),
                           Newsbox.active_start_fr <= datetime.utcnow())).
                 where(or_(Newsbox.active_end_de <= datetime.utcnow(),
                           Newsbox.active_end_en <= datetime.utcnow(),
                           Newsbox.active_end_fr <= datetime.utcnow()))]

    results = session.exec(statement[0])

    for res in results.all():

        if res.title_de == '&nbsp;' or res.title_en == '&nbsp;' or res.title_fr == '&nbsp;':
            continue

        if res.level == 2 and res.site_uuid == UUID('9c92af4f-6e95-4391-86d5-76eb8ad48360'):
            obj_level = 1  # rate UniBE Portal News higher - see order_by(NewsEvents.level) in routers/newsevents
        else:
            obj_level = res.level  # must always be >=2, because TeaserElement2022 are always be placed in a container

        obj = NewsEvents()
        obj.uuid = res.uuid
        obj.site_uuid = res.site_uuid
        obj.active_de = res.active_de
        obj.active_en = res.active_en
        obj.active_fr = res.active_fr
        obj.lastmod_dt_de = res.lastmod_dt_de
        obj.lastmod_dt_en = res.lastmod_dt_en
        obj.lastmod_dt_fr = res.lastmod_dt_fr

        obj.title_de = res.title_de
        obj.title_en = res.title_en
        obj.title_fr = res.title_fr
        obj.type = res.type
        obj.path = res.path
        obj.level = obj_level
        obj.start_dt = res.start_dt
        obj.end_dt = res.end_dt

        obj.url_de = res.url_de
        obj.url_en = res.url_en
        obj.url_fr = res.url_fr
        obj.infos_de = res.text_de
        obj.infos_en = res.text_en
        obj.infos_fr = res.text_fr
        obj.topics_de = res.topic_de
        obj.topics_en = res.topic_en
        obj.topics_fr = res.topic_fr
        obj.image_de = res.img
        obj.image_en = res.img
        obj.image_fr = res.img

        session.add(obj)
    session.commit()
