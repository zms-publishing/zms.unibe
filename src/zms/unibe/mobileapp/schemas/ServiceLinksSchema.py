from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ServiceLink(BaseModel):
    title: str
    url: str | None
    info: str | None
    path: str
    uuid: UUID
    lastmod: datetime
