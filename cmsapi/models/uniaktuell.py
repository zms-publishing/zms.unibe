from sqlmodel import Field, Column, DateTime
from datetime import date

from .zmsobjects import ZMSBase


class UniaktuellArticle(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=UniaktuellArticle&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    publish_dt_de: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    publish_dt_en: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    publish_dt_fr: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @staticmethod
    def get_zms_metaid():
        return 'UniaktuellArticle'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
            'publish_dt_de':    'publishdate',
            'publish_dt_en':    'publishdate',
            'publish_dt_fr':    'publishdate',
        }
