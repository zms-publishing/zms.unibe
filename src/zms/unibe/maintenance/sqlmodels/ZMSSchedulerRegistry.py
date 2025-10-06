from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, Column, DateTime

from zms.unibe.utils.helpers import parse_uuid


class ZMSSchedulerRegistry(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)
    task_uuid: UUID
    task_path: str
    task_title: str | None
    exec_onchange: bool = False
    exec_zms2sql: bool = False
    exec_opensearch: bool = False
    added_dt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    processed_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSScheduler'}

    @classmethod
    def get_attr_mapping_agenda(cls, obj):
        mapping = {
            'id':               None,
            'task_uuid':        parse_uuid(obj._uid),
            'task_path':        obj.getPath(),
            'task_title':       obj.attr('outlookid'),
            'exec_onchange':    True,
            'exec_zms2sql':     False,
            'exec_opensearch':  False,
            'added_dt':         datetime.now(),
            'processed_dt':     None,
        }
        return cls.model_validate(mapping)
