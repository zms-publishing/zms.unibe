from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime


class StatusMessage(SQLModel, table=True):  # to import data of http://id.unibe.ch/statusmeldungen provided by https://api.epc.unibe.ch/announcements/api/ServiceAnnouncements
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    begin: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    type: str
    subject: str
    description: str
    service: str
    info: str | None
