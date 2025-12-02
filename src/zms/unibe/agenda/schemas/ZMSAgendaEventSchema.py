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
    fileExtension: str | None
    fileSize: str


class ZMSAgendaEventSchema(BaseModel):
    eventId: str | None
    eventSource: str
    eventTitle: str
    eventAttachments: list[ZMSAgendaEventAttachmentSchema] | None
    eventAllDay: bool | None

    eventBeginDateTime: datetime
    eventBeginDate: str
    eventBeginTime: str
    eventBeginDay: int
    eventBeginDayWeek: str

    eventEndDateTime: datetime | None
    eventEndDate: str | None
    eventEndTime: str | None
    eventEndDay: int | None
    eventEndDayWeek: str | None

    eventLocation: str | None
    eventCategories: list | None
    eventInfos: str | None
    eventInfosPreview: str | None
    eventTagline: str | None
    eventImage: str | None
    eventUrl: str | None
