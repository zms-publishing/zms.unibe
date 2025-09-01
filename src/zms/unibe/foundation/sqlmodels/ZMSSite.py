from uuid import UUID

from sqlmodel import SQLModel, Field


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

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'domain':           'obj.getConfProperty(UniBE.Server)',
            'alias':            'obj.getConfProperty(UniBE.Alias)',
            'level':            'obj.getLevel()',
            'path':             'obj.getPath()',
            'type':             'obj.getType()',
            'theme':            'obj.getConfProperty(ZMS.theme)',
            'count_objs':       'obj.getCount()',
            'parent_uuid':      'obj.getParentHome()._uid'
        }
