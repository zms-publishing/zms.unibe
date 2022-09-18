from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID


class Newsbox(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    title_de: str
    title_en: str
    boxtype: str | None
    attr_event_start: datetime | None  # = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    attr_dc_subject_topic: str | None
    attr_url: str | None
    site_uuid: UUID = Field(foreign_key="zmssite.uuid")


class TeaserElement2022(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    title_de: str
    title_en: str
    attr_event_start: datetime | None  # = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    attr_dc_subject_topic: datetime | None
    attr_url: datetime | None
    site_uuid: UUID = Field(foreign_key="zmssite.uuid")
