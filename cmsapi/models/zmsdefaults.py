from sqlmodel import SQLModel, Field
from uuid import UUID


class ZMSSite(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    title_de: str
    title_en: str
    domain: str | None
    type: str


class ZMSFolder(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    title_de: str
    title_en: str
    type: str
    site_uuid: UUID = Field(foreign_key="zmssite.uuid")


class ZMSDocument(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    title_de: str
    title_en: str
    type: str
    site_uuid: UUID = Field(foreign_key="zmssite.uuid")
