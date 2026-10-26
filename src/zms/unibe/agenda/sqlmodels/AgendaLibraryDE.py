from sqlmodel import Field, SQLModel

from ...utils.types import OptionalDateTime, PostgreSQLArray


class AgendaLibraryDE(SQLModel, table=True):  # to import https://agenda.ub.unibe.ch/de/api/event
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    title: str
    eventType: str
    subjects: PostgreSQLArray
    series: str | None = None
    venue: str
    startsAt: OptionalDateTime
    endsAt: OptionalDateTime
    url: str
