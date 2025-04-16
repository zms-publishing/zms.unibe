from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Section(BaseModel):
    domain: str                     # ZMS subdomain
    title: str                      # ZMS gettitle
    type: str                       # ZMS sitetype
    path: str | None                # ZMS sitepath
    uuid: UUID | None               # ZMS siteuuid


class SectionResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[Section]


                                    # TODO: move this mapping overview to README
class News(BaseModel):              # TEASER ELEMENT 2022
    title: str                      # title
    date: datetime                  # ZMS lastmod_dt

    url: str | None                 # url
    infos: str | None               # text + source
    topics: str | None              # topic
    image: str | None               # img

    section: Section

    dataSource: str                 # ZMS path
    dataLevel: int                  # ZMS getlevel
    dataSort: int                   # ZMS getSortId
    dataSortParent: int             # ZMS getSortId of enclosing container
    dataUuid: UUID                  # ZMS uuid


class NewsResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[News]


class Event(BaseModel):             # TEASER ELEMENT 2022   AGENDA PORTAL                   AGENDA LIBRARY
    title: str                      # title                 veranstaltung_titel             title
    start: datetime                 # event_date_start      json_datum_zeit_start           startsAt
    end: datetime | None            # event_date_end        json_datum_zeit_end             endsAt
    location: str | None            # event_location        veranstaltung_horsaal           venue
                                    #                       + veranstaltung_gebaude_adresse
                                    #                       + veranstaltung_ort

    url: str | None                 # url                   veranstalter_info_link          url
    infos: str | None               # text + source         veranstaltung_referenten        subjects [list]
    topics: str | None              # topic                 veranstaltung_zyklus            event-type => eventType
    image: str | None               # img                   -                               -

    section: Section

    dataSource: str                 # ZMS getPath           agenda.unibe.ch/agenda.json     https://agenda.ub.unibe.ch/.
    dataLevel: int                  # ZMS getlevel          1                               1
    dataUuid: UUID | None           # ZMS uuid              -                               -


class EventResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[Event]


class StatusMessage(BaseModel):
    title: str                      # "subject": "Aktualisierung des Telefoniesystems",
    start: datetime                 # "begin": "2021-02-23T05:00:00",
    end: datetime | None            # "end": "2021-02-25T22:00:00",

    infos: str | None               # "description": "Die Komponenten des Telefoniesystems (Avaya Aura) werden auf die neusten Softwareversionen aktualisiert. Weitere Wartungsfenster folgen.\r\n\r\nTrotz der Redundanz der Systeme k\u00f6nnten kurze Performance-Einbussen oder minimale Unterbr\u00fcche entstehen.",
                                    # "info": "Gegebenenfalls verlangen einzelne Deskphones sich neu anzumelden. Dazu sind die Zugangsdaten gem\u00e4ss Bedienungsanleitung einzugeben. www.telecom.unibe.ch/bedienungsanleitungen"
    topics: str | None              # "service": "Telefonie +41 31 631 xx xx",

    section: Section                # "type": "WARTUNG",

    dataSource: str
    dataLevel: int
    dataUuid: UUID | None


class StatusMessageResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[StatusMessage]
