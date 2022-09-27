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
    topic: str
    level: int
    lastmod: datetime
    subdomain: str
    site_type: str
    site: str


class Event(BaseModel):
    uuid: UUID
    title: str
    topic: str
    start_dt: datetime
    end_dt: datetime | None
    level: int
    lastmod: datetime
    subdomain: str
    site_type: str
    site: str
