from uuid import UUID

from sqlmodel import SQLModel, Field
from .ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, \
    get_type, get_children_count, get_parent_home_uuid


class ZMSSite(SQLModel, table=True):  # http://localhost:5003/v3/zms/models?metaobj=ZMS&types=%2A
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    active_de: bool
    active_en: bool
    active_fr: bool
    title_de: str
    title_en: str
    title_fr: str
    domain: str | None
    alias: str | None
    level: int
    path: str
    type: str
    theme: str
    count_objs: int
    parent_uuid: UUID

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMS'}
    
    @classmethod
    def from_zms_obj(cls, obj):
        dict = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr      # zms_attr
            'title_de':     get_attr(obj, 'title', 'ger'),
            'title_en':     get_attr(obj, 'title', 'eng'),
            'title_fr':     get_attr(obj, 'title', 'fra'),
            'domain':       obj.getConfProperty('UniBE.Server'),
            'alias':        obj.getConfProperty('UniBE.Alias'),
            'type':         get_type(obj),
            'theme':        obj.getConfProperty('ZMS.theme'),
            'count_objs':   get_children_count(obj),
            'parent_uuid':  get_parent_home_uuid(obj)
        }
        return cls.model_validate(dict)
