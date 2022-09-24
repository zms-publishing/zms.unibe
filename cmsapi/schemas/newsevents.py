from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Site(BaseModel):
    uuid: UUID
    site: str
    type: str
    title: str
    subdomain: str


class News(BaseModel):
    uuid: UUID
    title: str
    level: int
    lastmod: datetime


class Event(BaseModel):
    uuid: UUID
    title: str
    level: int
    lastmod: datetime
