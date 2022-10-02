from pydantic import BaseModel
from uuid import UUID


class UniaktuellArticle(BaseModel):  # TODO: Response schema
    uuid: UUID
    title: str
    site: str | None
