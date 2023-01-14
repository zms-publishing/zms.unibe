from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ServiceLink(BaseModel):
    title: str
    url: str | None
    info: str | None
    path: str
    uuid: UUID
    lastmod: datetime
