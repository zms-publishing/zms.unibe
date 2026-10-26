from datetime import date
from uuid import UUID

from pydantic import BaseModel

from ...mobileapp.schemas.NewsEventsSchema import Section


class MediaNews(BaseModel):
    title: str                      # title
    date: date | None               # media_date

    infos: str | None               # media_lead
    topics: str | None              # attr_schlagworte
    categories: list[str] | None 
    image: str | None               # teaser_image
    url: str | None                 # url

    section: Section

    dataSource: str                 # ZMS path
    dataLevel: int                  # ZMS getlevel
    dataUuid: UUID                  # ZMS uuid


class MediaNewsResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[MediaNews]
