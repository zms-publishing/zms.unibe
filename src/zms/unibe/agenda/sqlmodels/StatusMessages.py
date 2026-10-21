from sqlmodel import Field, SQLModel

from ...utils.types import OptionalUTCNow


class StatusMessage(SQLModel, table=True):  # to import data of http://id.unibe.ch/statusmeldungen provided by https://api.epc.unibe.ch/announcements/api/ServiceAnnouncements
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    begin: OptionalUTCNow
    end: OptionalUTCNow
    type: str
    subject: str
    description: str
    service: str
    info: str | None
