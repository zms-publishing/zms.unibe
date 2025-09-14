from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_size


class UniBEFactsheet(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    titleimg_de: str | None
    titleimg_en: str | None
    titleimg_fr: str | None
    titleimg_size_de: str | None
    titleimg_size_en: str | None
    titleimg_size_fr: str | None
    elements: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'UniBEFactsheet'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'titleimg_de':      get_url(obj, 'titleimage', 'ger'),
            'titleimg_en':      get_url(obj, 'titleimage', 'eng'),
            'titleimg_fr':      get_url(obj, 'titleimage', 'fra'),
            'titleimg_size_de': get_size(obj, 'titleimage', 'ger'),
            'titleimg_size_en': get_size(obj, 'titleimage', 'eng'),
            'titleimg_size_fr': get_size(obj, 'titleimage', 'fra'),
            'elements':         obj.getObjChildren('e'),  # TODO: check this - or use get_children_count(obj)?
        }
        return cls.model_validate(mapping)
