# Provide data in frontends of unibe.ch
#
# for users/visitors (web) -> layout/design
# unibe-cms/frontend/web/estatico-handlebars/src/pages/portal-vk
# unibe-cms/frontend/web/estatico-handlebars/src/pages/portal-vk-v1
# unibe-cms/frontend/web/estatico-handlebars/src/pages/portal-vk-v2
# unibe-cms/frontend/zms/datatables/agenda
#
# for editors/managers (zmi) -> edit/manage
# unibe-cms/frontend/zms/models/unibe/metaobj_manager/ch.unibe.datatable/ZMSAgenda
#
# see overview of data mapping in
# zms-addons/src/zms/unibe/agenda/schemas/README.md

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    eventTitle: str
    eventStart: datetime
    eventEnd: datetime | None
    eventLocation: str | None
    
    eventTopics: list | None
    eventInfos: str | None
    eventImage: str | None
    eventUrl: str | None
    
    eventSource: str
    eventId: UUID | None
