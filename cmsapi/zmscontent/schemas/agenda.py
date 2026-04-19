from pydantic import BaseModel
from zms.unibe.agenda.schemas.ZMSAgendaEventSchema import ZMSAgendaEventSchema


# TODO: this is an example to prove the concept with ZMSAgendaResponse
class ZMSAgendaResponse(BaseModel):
    offset: int
    limit: int
    total: int
    locale: str
    site_path: str
    content_model: str
    data_schema: dict | None
    data_items: list[ZMSAgendaEventSchema]
