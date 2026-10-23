from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_size, get_url


class Hero(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img: str | None = None
    img_size: int | None = None
    name_de: str
    name_en: str
    name_fr: str
    title_de: str | None = None
    title_en: str | None = None
    title_fr: str | None = None
    quote_de: str | None = None
    quote_en: str | None = None
    quote_fr: str | None = None
    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None
    url_type_de: str | None = None
    url_type_en: str | None = None
    url_type_fr: str | None = None
    url_title_de: str | None = None
    url_title_en: str | None = None
    url_title_fr: str | None = None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'hero'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'img':              get_url(obj,'hero_image'),
            'img_size':         get_size(obj, 'hero_image'),
            'name_de':          get_attr(obj, 'hero_name', 'ger'),
            'name_en':          get_attr(obj, 'hero_name', 'eng'),
            'name_fr':          get_attr(obj, 'hero_name', 'fra'),
            'title_de':         get_attr(obj, 'hero_title', 'ger'),
            'title_en':         get_attr(obj, 'hero_title', 'eng'),
            'title_fr':         get_attr(obj, 'hero_title', 'fra'),
            'quote_de':         get_attr(obj, 'hero_quote', 'ger'),
            'quote_en':         get_attr(obj, 'hero_quote', 'eng'),
            'quote_fr':         get_attr(obj, 'hero_quote', 'fra'),
            'url_de':           get_url(obj, 'url', 'ger'),
            'url_en':           get_url(obj, 'url', 'eng'),
            'url_fr':           get_url(obj, 'url', 'fra'),
            'url_type_de':      get_attr(obj, 'url_type', 'ger'),
            'url_type_en':      get_attr(obj, 'url_type', 'eng'),
            'url_type_fr':      get_attr(obj, 'url_type', 'fra'),
            'url_title_de':     get_attr(obj, 'url_title', 'ger'),
            'url_title_en':     get_attr(obj, 'url_title', 'eng'),
            'url_title_fr':     get_attr(obj, 'url_title', 'fra'),
        }
        return cls.model_validate(mapping)
