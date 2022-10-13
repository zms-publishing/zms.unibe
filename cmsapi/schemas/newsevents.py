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


class StatusMessage(BaseModel):
    statusTitle: str                # "subject": "Aktualisierung des Telefoniesystems",
    statusStart: datetime           # "begin": "2021-02-23T05:00:00",
    statusEnd: datetime | None      # "end": "2021-02-25T22:00:00",

    statusInfos: str | None         # "description": "Die Komponenten des Telefoniesystems (Avaya Aura) werden auf die neusten Softwareversionen aktualisiert. Weitere Wartungsfenster folgen.\r\n\r\nTrotz der Redundanz der Systeme k\u00f6nnten kurze Performance-Einbussen oder minimale Unterbr\u00fcche entstehen.",
                                    # "info": "Gegebenenfalls verlangen einzelne Deskphones sich neu anzumelden. Dazu sind die Zugangsdaten gem\u00e4ss Bedienungsanleitung einzugeben. www.telecom.unibe.ch/bedienungsanleitungen"
    statusTopics: str | None        # "type": "WARTUNG",
                                    # "service": "Telefonie +41 31 631 xx xx",
    sectionDomain: str
    sectionTitle: str
    sectionType: str

    dataSource: str
    dataLevel: str
    dataUuid: UUID | None
