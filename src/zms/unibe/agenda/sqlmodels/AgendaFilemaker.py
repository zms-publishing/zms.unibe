from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime


class AgendaFilemaker(SQLModel, table=True):  # to import https://agenda.unibe.ch/agenda.json
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    json_datum_zeit_start: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    json_datum_zeit_end: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    veranstaltung_zyklus: str
    veranstaltung_titel: str
    veranstaltung_referenten: str
    veranstaltung_gebaude_adresse: str
    veranstaltung_horsaal: str
    veranstaltung_ort: str
    veranstalter_info_link: str
