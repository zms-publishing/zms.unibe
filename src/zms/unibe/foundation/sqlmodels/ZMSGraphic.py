from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_size


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
    img_size_de: int | None
    img_size_en: int | None
    img_size_fr: int | None
    imghires_size_de: int | None
    imghires_size_en: int | None
    imghires_size_fr: int | None
    imgsuperres_size_de: int | None
    imgsuperres_size_en: int | None
    imgsuperres_size_fr: int | None
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
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSGraphic'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr              # zms_attr
            'descr_de':             get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':             get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':             get_attr(obj, 'attr_dc_description', 'fra'),
            'img_de':               get_url(obj, 'img', 'ger'),
            'img_en':               get_url(obj, 'img', 'eng'),
            'img_fr':               get_url(obj, 'img', 'fra'),
            'imghires_de':          get_url(obj, 'imghires', 'ger'),
            'imghires_en':          get_url(obj, 'imghires', 'eng'),
            'imghires_fr':          get_url(obj, 'imghires', 'fra'),
            'imgsuperres_de':       get_url(obj, 'imgsuperres', 'ger'),
            'imgsuperres_en':       get_url(obj, 'imgsuperres', 'eng'),
            'imgsuperres_fr':       get_url(obj, 'imgsuperres', 'fra'),
            'img_size_de':          get_size(obj, 'img', 'ger'),
            'img_size_en':          get_size(obj, 'img', 'eng'),
            'img_size_fr':          get_size(obj, 'img', 'fra'),
            'imghires_size_de':     get_size(obj, 'imghires', 'ger'),
            'imghires_size_en':     get_size(obj, 'imghires', 'eng'),
            'imghires_size_fr':     get_size(obj, 'imghires', 'fra'),
            'imgsuperres_size_de':  get_size(obj, 'imgsuperres', 'ger'),
            'imgsuperres_size_en':  get_size(obj, 'imgsuperres', 'eng'),
            'imgsuperres_size_fr':  get_size(obj, 'imgsuperres', 'fra'),
            'img_attrs_spec':       obj.attr('img_attrs_spec'),
            'attr_url_de':          get_url(obj, 'attr_url', 'ger'),
            'attr_url_en':          get_url(obj, 'attr_url', 'eng'),
            'attr_url_fr':          get_url(obj, 'attr_url', 'fra'),
            'text_de':              get_attr(obj, 'text', 'ger'),
            'text_en':              get_attr(obj, 'text', 'eng'),
            'text_fr':              get_attr(obj, 'text', 'fra'),
            'captionaddon_de':      get_attr(obj, 'captionaddon', 'ger'),
            'captionaddon_en':      get_attr(obj, 'captionaddon', 'eng'),
            'captionaddon_fr':      get_attr(obj, 'captionaddon', 'fra'),
        }
        return cls.model_validate(mapping)
