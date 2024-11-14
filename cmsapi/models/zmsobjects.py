from sqlmodel import SQLModel, Field, Column, DateTime, JSON
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import UUID


class ZMSBase(SQLModel, table=False):  # Base class from which ZMSObjects inherit
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid")
    active_de: bool
    active_en: bool
    active_fr: bool
    active_start_de: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    active_start_en: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    active_start_fr: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    active_end_de: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    active_end_en: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    active_end_fr: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    created_dt_de: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    created_dt_en: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    created_dt_fr: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    lastmod_dt_de: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    lastmod_dt_en: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    lastmod_dt_fr: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
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
            'active_de':        'active_ger',
            'active_en':        'active_eng',
            'active_fr':        'active_fra',
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
    parent_uuid: UUID

    @staticmethod
    def get_zms_metaid():
        return 'ZMS'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'domain':           "obj.getConfProperty('UniBE.Server')",
            'alias':            "obj.getConfProperty('UniBE.Alias')",
            'level':            'obj.getLevel()',
            'path':             'obj.getPath()',
            'type':             'obj.getType()',
            'parent_uuid':      'obj.getParentHome()._uid'
        }


class ZMSFolder(ZMSBase, table=True):  # TODO: http://localhost:5003/v3/zms/models?metaobj=ZMSFolder&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFolder'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'attr_dc_type',
        }


class ZMSDocument(ZMSBase, table=True):  # TODO: http://localhost:5003/v3/zms/models?metaobj=ZMSDocument&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDocument'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'attr_dc_type',
        }


class ZMSFormulator(ZMSBase, table=True):  # TODO: http://localhost:5003/v3/zms/models?metaobj=ZMSFormulator&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFormulator'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
        }


class ZMSBoris(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    dataurl: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    boris_data: str | None  # = Field(sa_column=Column(JSONB), default_factory=dict)

    @staticmethod
    def get_zms_metaid():
        return 'ZMSBoris'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'dataurl': 'dataurl',
            'descr_de': 'attr_dc_description_ger',
            'descr_en': 'attr_dc_description_eng',
            'descr_fr': 'attr_dc_description_fra',
            'boris_data': '_datafilecached',
        }


class ZMSDataTable(ZMSBase, table=True):  # TODO: http://localhost:5003/v3/zms/models?metaobj=ZMSDataTable&types=%2A
    __table_args__ = {'extend_existing': True}
    dataurl: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDataTable'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'dataurl':          'dataurl',
        }


class ZMSGraphic(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    imghires_de: str | None
    imghires_en: str | None
    imghires_fr: str | None
    imgsuperres_de: str | None
    imgsuperres_en: str | None
    imgsuperres_fr: str | None
    img_attrs_spec: str | None
    attr_url_de: str | None
    attr_url_en: str | None
    attr_url_fr: str | None
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    captionaddon_de: str | None
    captionaddon_en: str | None
    captionaddon_fr: str | None
    
    @staticmethod
    def get_zms_metaid():
        return 'ZMSGraphic'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr

            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'img_de':           'img_ger',
            'img_en':           'img_eng',
            'img_fr':           'img_fra',
            'imghires_de':      'imghires_ger',
            'imghires_en':      'imghires_eng',
            'imghires_fr':      'imghires_fra',
            'imgsuperres_de':   'imgsuperres_ger',
            'imgsuperres_en':   'imgsuperres_eng',
            'imgsuperres_fr':   'imgsuperres_fra',
            'img_attrs_spec':   'img_attrs_spec',
            'attr_url_de':      'attr_url_ger',
            'attr_url_en':      'attr_url_eng',
            'attr_url_fr':      'attr_url_fra',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'captionaddon_de':  'captionaddon_ger',
            'captionaddon_en':  'captionaddon_eng',
            'captionaddon_fr':  'captionaddon_fra',
        }


class TwoCols(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'twocols'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
        }

class ContentTabs(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    layout: str | None
    orientation: str | None

    @staticmethod
    def get_zms_metaid():
        return 'contenttabs'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'layout':           'attr_dc_type_layout',
            'orientation':      'orientation',
        }

class InfoBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    anchor: str | None
    img: str | None
    img_attrs_spec: str | None
    copyright_de: str | None
    copyright_en: str | None
    copyright_fr: str | None
    layout: str | None

    @staticmethod
    def get_zms_metaid():
        return 'infobox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'anchor':           'ankername',
            'img':              'img',
            'img_attrs_spec':   'img_attrs_spec',
            'copyright_de':     'captionaddon_ger',   
            'copyright_en':     'captionaddon_eng',   
            'copyright_fr':     'captionaddon_fra',
            'layout':           'attr_dc_type_layout',
        }