from uuid import UUID

from sqlmodel import Field, SQLModel

from ...utils.types import OptionalDateTime


class NewsEvents(SQLModel, table=True):  # intermediate consolidation of Agendas, NewsBox, TeaserElement2022 for queries
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid", ondelete="CASCADE")
    active_de: bool
    active_en: bool
    active_fr: bool
    lastmod_dt_de: OptionalDateTime
    lastmod_dt_en: OptionalDateTime
    lastmod_dt_fr: OptionalDateTime

    title_de: str | None = None
    title_en: str | None = None
    title_fr: str | None = None
    type: str | None = None
    allday: bool | None = None
    id: str | None = None
    source: str | None = None
    path: str
    level: int
    sort_id: int
    sort_id_parent: int
    start_dt: OptionalDateTime
    end_dt: OptionalDateTime
    location_de: str | None = None
    location_en: str | None = None
    location_fr: str | None = None

    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None
    infos_de: str | None = None
    infos_en: str | None = None
    infos_fr: str | None = None
    topics_de: str | None = None
    topics_en: str | None = None
    topics_fr: str | None = None
    image_de: str | None = None
    image_en: str | None = None
    image_fr: str | None = None
