from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel, Field, Column, DateTime


class NewsEvents(SQLModel, table=True):  # intermediate consolidation of Agendas, NewsBox, TeaserElement2022 for queries
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid", ondelete="CASCADE")
    active_de: bool
    active_en: bool
    active_fr: bool
    lastmod_dt_de: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    lastmod_dt_en: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    lastmod_dt_fr: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    title_de: str | None
    title_en: str | None
    title_fr: str | None
    type: str | None
    allday: bool | None
    id: str | None
    source: str | None
    path: str
    level: int
    sort_id: int
    sort_id_parent: int
    start_dt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end_dt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    location_de: str | None
    location_en: str | None
    location_fr: str | None

    url_de: str | None
    url_en: str | None
    url_fr: str | None
    infos_de: str | None
    infos_en: str | None
    infos_fr: str | None
    topics_de: str | None
    topics_en: str | None
    topics_fr: str | None
    image_de: str | None
    image_en: str | None
    image_fr: str | None
