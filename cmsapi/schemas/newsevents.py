from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


                                    # TODO: move this mapping overview to README
class News(BaseModel):              # TEASER ELEMENT 2022
    newsTitle: str                  # title
    newsDate: datetime              # ZMS lastmod_dt

    newsUrl: str | None             # url
    newsInfos: str | None           # text + source
    newsTopics: str | None          # topic
    newsImage: str | None           # img

    sectionDomain: str              # ZMS subdomain
    sectionTitle: str               # ZMS gettitle
    sectionType: str                # ZMS sitetype

    dataSource: str                 # ZMS path
    dataLevel: str                  # ZMS getlevel
    dataUuid: UUID                  # ZMS uuid


class Event(BaseModel):             # TEASER ELEMENT 2022   AGENDA PORTAL                   AGENDA LIBRARY
    eventTitle: str                 # title                 veranstaltung_titel             title
    eventStart: datetime            # event_date_start      json_datum_zeit_start           startsAt
    eventEnd: datetime | None       # event_date_end        json_datum_zeit_end             endsAt
    eventLocation: str              # event_location        veranstaltung_horsaal           venue
                                    #                       + veranstaltung_gebaude_adresse
                                    #                       + veranstaltung_ort

    eventUrl: str | None            # url                   veranstalter_info_link          url
    eventInfos: str | None          # text + source         veranstaltung_referenten        subjects [list]
    eventTopics: str | None         # topic                 veranstaltung_zyklus            event-type => eventType
    eventImage: str | None          # img                   -                               -

    sectionDomain: str              # ZMS subdomain         ZMS subdomain                   ZMS subdomain
    sectionTitle: str               # ZMS gettitle          ZMS gettitle                    ZMS gettitle
    sectionType: str                # ZMS sitetype          Portal                          Library

    dataSource: str                 # ZMS getPath           agenda.unibe.ch/agenda.json     https://agenda.ub.unibe.ch/.
    dataLevel: str                  # ZMS getlevel          1                               1
    dataUuid: UUID | None           # ZMS uuid              -                               -


class Section(BaseModel):
    sectionDomain: str
    sectionTitle: str
    sectionType: str
    sectionPath: str
    sectionUuid: UUID
