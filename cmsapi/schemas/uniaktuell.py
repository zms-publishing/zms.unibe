from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
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
    dataLevel: str                  # ZMS getlevel
    dataUuid: UUID                  # ZMS uuid


class UniaktuellArticleResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[UniaktuellArticle]
