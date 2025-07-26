# ZMSAgenda Data Schema
#
# see mapping overview of different data sources
# unibe-cms/backend/zms-addons/src/zms/unibe/agenda/schemas/README.md
#
# Frontend functionality -> layout/design -> frontend for users/visitors (web)
# http://localhost:9000/pages/portal-agenda/portal-agenda.html
# unibe-cms/frontend/web/estatico-handlebars/src/modules/agenda/agenda.hbs
# unibe-cms/frontend/web/estatico-handlebars/src/modules/date_badge/date_badge.hbs
#
# Backend functionality -> edit/manage -> frontend for editors/managers (zmi)
# unibe-cms/backend/zms-addons/src/zms/unibe/agenda
# unibe-cms/frontend/zms/models/unibe/metaobj_manager/ch.unibe.datatable/ZMSAgenda
# unibe-cms/frontend/zms/models/unibe/metaobj_manager/ch.unibe.datatable/ZMSAgenda/agenda.zpt


from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    eventId: UUID | None
    eventSource: str
    eventTitle: str

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
