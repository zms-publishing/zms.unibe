from sqlmodel import Field, SQLModel

from ...utils.types import OptionalDateTime


class AgendaFilemaker(SQLModel, table=True):  # to import https://agenda.unibe.ch/agenda.json
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    json_datum_zeit_start: OptionalDateTime
    json_datum_zeit_end: OptionalDateTime
    veranstaltung_zyklus: str
    veranstaltung_titel: str
    veranstaltung_referenten: str
    veranstaltung_gebaude_adresse: str
    veranstaltung_horsaal: str
    veranstaltung_ort: str
    veranstalter_info_link: str
