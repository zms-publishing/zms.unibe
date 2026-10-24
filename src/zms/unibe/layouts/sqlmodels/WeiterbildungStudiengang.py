from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.zms2sql.getters import get_attr, get_children_count, get_size, get_url


class WeiterbildungStudiengang(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None = None
    title_en: str | None = None
    title_fr: str | None = None
    category: str | None = None
    subject_de: str | None = None
    subject_en: str | None = None
    subject_fr: str | None = None
    descr_de: str | None = None
    descr_en: str | None = None
    descr_fr: str | None = None
    img: str | None = None
    img_size: int | None = None
    titleimg_de: str | None = None
    titleimg_en: str | None = None
    titleimg_fr: str | None = None
    titleimg_size_de: int | None = None
    titleimg_size_en: int | None = None
    titleimg_size_fr: int | None = None
    elements: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'weiterbildung_studiengang'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'category':         obj.attr('rubrik'),
            'subject_de':       get_attr(obj, 'attr_dc_subject', 'ger'),
            'subject_en':       get_attr(obj, 'attr_dc_subject', 'eng'),
            'subject_fr':       get_attr(obj, 'attr_dc_subject', 'fra'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'img':              get_url(obj, 'article_teaserbild'),
            'img_size':         get_size(obj, 'article_teaserbild'),
            'titleimg_de':      get_url(obj, 'titleimage', 'ger'),
            'titleimg_en':      get_url(obj, 'titleimage', 'eng'),
            'titleimg_fr':      get_url(obj, 'titleimage', 'fra'),
            'titleimg_size_de': get_size(obj, 'titleimage', 'ger'),
            'titleimg_size_en': get_size(obj, 'titleimage', 'eng'),
            'titleimg_size_fr': get_size(obj, 'titleimage', 'fra'),
            'elements':         get_children_count(obj),
        }
        return cls.model_validate(mapping)
