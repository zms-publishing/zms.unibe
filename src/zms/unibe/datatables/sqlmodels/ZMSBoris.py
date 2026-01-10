from datetime import datetime
from sqlmodel import Field, Column, DateTime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_data, parse_datetime


class ZMSBoris(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    dataurl: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    boris_data: str | None  # = Field(sa_column=Column(JSONB), default_factory=dict)
    lastupdate: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSBoris'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'dataurl':          get_url(obj, 'dataurl'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'boris_data':       get_data(obj, '_datafilecached', json_as_py=False)[0],
            'lastupdate':       parse_datetime(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
