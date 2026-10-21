from sqlmodel import Field, SQLModel

from ...utils.types import OptionalUTCNow, PostgreSQLArray


class AgendaLibraryEN(SQLModel, table=True):  # to import https://agenda.ub.unibe.ch/en/api/event
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    title: str
    eventType: str
    subjects: PostgreSQLArray
    series: str | None
    venue: str
    startsAt: OptionalUTCNow
    endsAt: OptionalUTCNow
    url: str
