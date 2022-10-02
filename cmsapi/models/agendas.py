from sqlmodel import SQLModel, Field, Column, DateTime, String
from sqlalchemy.dialects import postgresql
from datetime import datetime


class AgendaPortal(SQLModel, table=True):  # to import https://agenda.unibe.ch/agenda.json
    __table_args__ = {'extend_existing': True}
    id: int = Field(primary_key=True)
    json_datum_zeit_start: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    json_datum_zeit_end: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    veranstaltung_zyklus: str
    veranstaltung_titel: str
    veranstaltung_referenten: str
    veranstaltung_gebaude_adresse: str
    veranstaltung_horsaal: str
    veranstaltung_ort: str
    veranstalter_info_link: str


class AgendaLibraryDE(SQLModel, table=True):  # to import https://agenda.ub.unibe.ch/de/api/event
    __table_args__ = {'extend_existing': True}
    id: int = Field(primary_key=True)
    title: str
    eventType: str
    subjects: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    venue: str
    startsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    endsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    url: str


class AgendaLibraryEN(SQLModel, table=True):  # to import https://agenda.ub.unibe.ch/en/api/event
    __table_args__ = {'extend_existing': True}
    id: int = Field(primary_key=True)
    title: str
    eventType: str
    subjects: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    venue: str
    startsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    endsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    url: str
