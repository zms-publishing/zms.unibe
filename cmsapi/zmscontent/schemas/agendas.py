# PLEASE NOTE: ZMSAgendaEvent* schemas are copied from External Method in
# unibe-cms/frontend/zms/models/unibe/metaobj_manager/ch.unibe.datatable/ZMSAgenda/ZMSAgenda.py
# -> this is an example to prove the concept

from datetime import datetime
from pydantic import BaseModel


class ZMSAgendaEventAttachmentSchema(BaseModel):
    id: str
    contentId: str | None  # TODO: needed to get bytes data of inline images...?! sometimes(?) no UUID but str
    contentType: str
    name: str
    size: int
    isInline: bool
    lastModifiedDateTime: datetime


class ZMSAgendaEventSchema(BaseModel):
    eventId: str | None
    eventSource: str
    eventTitle: str
    eventAttachments: list[ZMSAgendaEventAttachmentSchema] | None

    eventStartDateTime: datetime
    eventStartDate: str
    eventStartTime: str
    eventStartDay: int
    eventStartDayWeek: str

    eventEndDateTime: datetime | None
    eventEndDate: str | None
    eventEndTime: str | None
    eventEndDay: int | None
    eventEndDayWeek: str | None

    eventLocation: str | None
    eventTopics: list | None
    eventInfos: str | None
    eventImage: str | None
    eventUrl: str | None


class ZMSAgendaResponse(BaseModel):
    offset: int
    limit: int
    total: int
    data: list[ZMSAgendaEventSchema]
