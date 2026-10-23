from uuid import UUID

from sqlmodel import Field, SQLModel

from ...utils.helpers import (
    get_attr,
    get_level,
    get_parent_node_sort_id,
    is_activated_by_checkbox_and_timeline,
    local_timezone,
    parse_uuid,
)
from ...utils.types import OptionalDateTime


class ZMSBase(SQLModel, table=False):  # Base class from which ZMSObjects inherit
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid", ondelete="CASCADE")
    active_de: bool
    active_en: bool
    active_fr: bool
    active_start_de: OptionalDateTime
    active_start_en: OptionalDateTime
    active_start_fr: OptionalDateTime
    active_end_de: OptionalDateTime
    active_end_en: OptionalDateTime
    active_end_fr: OptionalDateTime
    created_dt_de: OptionalDateTime
    created_dt_en: OptionalDateTime
    created_dt_fr: OptionalDateTime
    lastmod_dt_de: OptionalDateTime
    lastmod_dt_en: OptionalDateTime
    lastmod_dt_fr: OptionalDateTime
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
            'active_start_de':  local_timezone(get_attr(obj, 'attr_active_start', 'ger')),
            'active_start_en':  local_timezone(get_attr(obj, 'attr_active_start', 'eng')),
            'active_start_fr':  local_timezone(get_attr(obj, 'attr_active_start', 'fra')),
            'active_end_de':    local_timezone(get_attr(obj, 'attr_active_end', 'ger')),
            'active_end_en':    local_timezone(get_attr(obj, 'attr_active_end', 'eng')),
            'active_end_fr':    local_timezone(get_attr(obj, 'attr_active_end', 'fra')),
            'created_dt_de':    local_timezone(get_attr(obj, 'created_dt', 'ger')),
            'created_dt_en':    local_timezone(get_attr(obj, 'created_dt', 'eng')),
            'created_dt_fr':    local_timezone(get_attr(obj, 'created_dt', 'fra')),
            'lastmod_dt_de':    local_timezone(get_attr(obj, 'change_dt', 'ger')),
            'lastmod_dt_en':    local_timezone(get_attr(obj, 'change_dt', 'eng')),
            'lastmod_dt_fr':    local_timezone(get_attr(obj, 'change_dt', 'fra')),
            'sort_id_parent':   get_parent_node_sort_id(obj),
            'sort_id':          obj.getSortId(),
            'level':            get_level(obj),
            'path':             obj.getPath(),
        }
