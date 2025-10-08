from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_size


class ZMSFile(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    file_de: str | None
    file_en: str | None
    file_fr: str | None
    file_size_de: int | None
    file_size_en: int | None
    file_size_fr: int | None
    filetype: str
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    amount_de: str | None
    amount_en: str | None
    amount_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSFile'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'file_de':          get_url(obj, 'file', 'ger'),
            'file_en':          get_url(obj, 'file', 'eng'),
            'file_fr':          get_url(obj, 'file', 'fra'),
            'file_size_de':     get_size(obj, 'file', 'ger'),
            'file_size_en':     get_size(obj, 'file', 'eng'),
            'file_size_fr':     get_size(obj, 'file', 'fra'),
            'filetype':         obj.attr('filetype'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'amount_de':        get_attr(obj, 'amount', 'ger'),
            'amount_en':        get_attr(obj, 'amount', 'eng'),
            'amount_fr':        get_attr(obj, 'amount', 'fra'),
        }
        return cls.model_validate(mapping)
