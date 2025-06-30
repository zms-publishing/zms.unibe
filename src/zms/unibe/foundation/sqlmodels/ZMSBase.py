from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel, Field, DateTime


class ZMSBase(SQLModel, table=False):  # Base class from which ZMSObjects inherit
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid", ondelete="CASCADE")
    active_de: bool
    active_en: bool
    active_fr: bool
    active_start_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_start_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_start_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    sort_id_parent: int
    sort_id: int
    level: int
    path: str

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'uuid':             'obj._uid',
            'site_uuid':        'obj.getDocumentElement()._uid',
            'active_de':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_en':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_fr':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_start_de':  'attr_active_start_ger',
            'active_start_en':  'attr_active_start_eng',
            'active_start_fr':  'attr_active_start_fra',
            'active_end_de':    'attr_active_end_ger',
            'active_end_en':    'attr_active_end_eng',
            'active_end_fr':    'attr_active_end_fra',
            'created_dt_de':    'created_dt_ger',
            'created_dt_en':    'created_dt_eng',
            'created_dt_fr':    'created_dt_fra',
            'lastmod_dt_de':    'change_dt_ger',
            'lastmod_dt_en':    'change_dt_eng',
            'lastmod_dt_fr':    'change_dt_fra',
            'sort_id_parent':   'obj.getParentNode().getSortId()',
            'sort_id':          'obj.getSortId()',
            'level':            'obj.getLevel()',
            'path':             'obj.getPath()',
        }
