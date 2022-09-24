from pydantic import BaseModel


class ZMSSite(BaseModel):
    site: str
    subdomain: str


class ZMSDataTable(BaseModel):
    site: str | None
    url: str | None
