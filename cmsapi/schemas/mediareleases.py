from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from ..schemas.newsevents import Section


class MediaRelease(BaseModel):
    title: str                      # title
    date: datetime | None           # media_date

    infos: str | None               # media_lead
    topics: str | None              # attr_schlagworte
    image: str | None               # teaser_image
    url: str | None                 # url

    section: Section

    dataSource: str                 # ZMS path
    dataLevel: int                  # ZMS getlevel
    dataUuid: UUID                  # ZMS uuid


class MediaReleaseResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[MediaRelease]
