from datetime import datetime

from sqlmodel import Field, DateTime

from ...foundation.sqlmodels.ZMSBase import ZMSBase


class ZMSBoris(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    dataurl: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    boris_data: str | None  # = Field(sa_column=Column(JSONB), default_factory=dict)
    lastupdate: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSBoris'}

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'dataurl':          'dataurl',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'boris_data':       'obj.getData(_datafilecached)',
            'lastupdate':       '_datalastupdated',
        }

