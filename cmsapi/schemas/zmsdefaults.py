from pydantic import BaseModel


class ZMSSite(BaseModel):
    subdomain: str
