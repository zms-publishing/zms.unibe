from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Service(BaseModel):
    serviceTitle: str
    serviceLink: str | None
    serviceInfo: str | None
    servicePath: str
    serviceUuid: UUID
    serviceLastmodified: datetime
