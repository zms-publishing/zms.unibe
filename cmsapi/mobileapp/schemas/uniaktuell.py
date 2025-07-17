from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..schemas.newsevents import Section


class UniaktuellArticle(BaseModel):
    title: str                      # title
    date: datetime | None           # publish_dt

    infos: str | None               # abstract
    topics: str | None              # category + topics
    image: str | None               # img
    url: str | None                 # url

    section: Section

    dataSource: str                 # ZMS path
    dataLevel: int                  # ZMS getlevel
    dataUuid: UUID                  # ZMS uuid


class UniaktuellArticleResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[UniaktuellArticle]
