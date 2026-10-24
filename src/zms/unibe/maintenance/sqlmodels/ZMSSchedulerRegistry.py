from uuid import UUID

from sqlmodel import Field, SQLModel

from ...helpers import local_timezone
from ...utils.types import OptionalDateTime
from ...utils.zms2sql.getters import parse_uuid


class ZMSSchedulerRegistry(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    task_uuid: UUID
    task_path: str
    task_title: str | None = None
    exec_onchange: bool = False
    exec_zms2sql: bool = False
    exec_opensearch: bool = False
    added_dt: OptionalDateTime
    processed_dt: OptionalDateTime = None

    @classmethod
    def from_agenda(cls, obj):
        mapping = {
            'id':               None,
            'task_uuid':        parse_uuid(obj._uid),
            'task_path':        obj.getPath(),
            'task_title':       obj.attr('outlook_upn'),
            'exec_onchange':    True,
            'exec_zms2sql':     False,
            'exec_opensearch':  False,
            'added_dt':         local_timezone(),
            'processed_dt':     None,
        }
        return cls.model_validate(mapping)
