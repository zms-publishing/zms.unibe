from sqlmodel import SQLModel, Field, Column, DateTime
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
    level: int

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'uuid':             'obj._uid',
            'site_uuid':        'obj.getDocumentElement()._uid',
            'active_de':        'active',
            'active_en':        'active',
            'active_fr':        'active',
            'active_start_de':  'attr_active_start',
            'active_start_en':  'attr_active_start',
            'active_start_fr':  'attr_active_start',
            'active_end_de':    'attr_active_end',
            'active_end_en':    'attr_active_end',
            'active_end_fr':    'attr_active_end',
            'created_dt_de':    'created_dt',
            'created_dt_en':    'created_dt',
            'created_dt_fr':    'created_dt',
            'lastmod_dt_de':    'change_dt',
            'lastmod_dt_en':    'change_dt',
            'lastmod_dt_fr':    'change_dt',
            'level':            'obj.getLevel()',
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
    path: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMS'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
            'domain':           "obj.getConfProperty('UniBE.Server')",
            'path':             "obj.getPath()",
            'type':             'attr_dc_type',
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
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
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
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
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
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
        }


class ZMSDataTable(ZMSBase, table=True):  # TODO: http://localhost:5003/v3/zms/models?metaobj=ZMSDataTable&types=%2A
    __table_args__ = {'extend_existing': True}
    path: str
    dataurl: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDataTable'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'dataurl':          'dataurl',
            'path':             'obj.getPath()',
        }
