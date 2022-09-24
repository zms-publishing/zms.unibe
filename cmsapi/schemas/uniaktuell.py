from pydantic import BaseModel
from uuid import UUID


class UniaktuellArticle(BaseModel):
    uuid: UUID
    title: str
    site: str | None
