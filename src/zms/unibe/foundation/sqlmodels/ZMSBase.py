from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field, DateTime
from zms.unibe.utils.helpers import (
    get_attr,
    get_level,
    get_parent_node_sort_id,
    is_activated_by_checkbox_and_timeline,
    parse_datetime,
    parse_uuid,
)


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
    def get_attr_mappings(obj):
        return {
            # sql_attr          # zms_attr
            'uuid':             parse_uuid(obj._uid),
            'site_uuid':        parse_uuid(obj.getDocumentElement()._uid),
            'active_de':        is_activated_by_checkbox_and_timeline(obj, 'ger'),
            'active_en':        is_activated_by_checkbox_and_timeline(obj, 'eng'),
            'active_fr':        is_activated_by_checkbox_and_timeline(obj, 'fra'),
            'active_start_de':  parse_datetime(get_attr(obj, 'attr_active_start', 'ger')),
            'active_start_en':  parse_datetime(get_attr(obj, 'attr_active_start', 'eng')),
            'active_start_fr':  parse_datetime(get_attr(obj, 'attr_active_start', 'fra')),
            'active_end_de':    parse_datetime(get_attr(obj, 'attr_active_end', 'ger')),
            'active_end_en':    parse_datetime(get_attr(obj, 'attr_active_end', 'eng')),
            'active_end_fr':    parse_datetime(get_attr(obj, 'attr_active_end', 'fra')),
            'created_dt_de':    parse_datetime(get_attr(obj, 'created_dt', 'ger')),
            'created_dt_en':    parse_datetime(get_attr(obj, 'created_dt', 'eng')),
            'created_dt_fr':    parse_datetime(get_attr(obj, 'created_dt', 'fra')),
            'lastmod_dt_de':    parse_datetime(get_attr(obj, 'change_dt', 'ger')),
            'lastmod_dt_en':    parse_datetime(get_attr(obj, 'change_dt', 'eng')),
            'lastmod_dt_fr':    parse_datetime(get_attr(obj, 'change_dt', 'fra')),
            'sort_id_parent':   get_parent_node_sort_id(obj),
            'sort_id':          obj.getSortId(),
            'level':            get_level(obj),
            'path':             obj.getPath(),
        }
