from datetime import datetime

from sqlalchemy.dialects import postgresql
from sqlmodel import SQLModel, Field, Column, DateTime, String


class AgendaLibraryEN(SQLModel, table=True):  # to import https://agenda.ub.unibe.ch/en/api/event
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    title: str
    eventType: str
    subjects: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    venue: str
    startsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    endsAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    url: str
