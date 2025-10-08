from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_size


class Hero2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img: str | None
    img_size: int | None
    video: str | None
    video_size: int | None
    overlay: bool
    img_alt_de: str | None
    img_alt_en: str | None
    img_alt_fr: str | None
    title_de: str
    title_en: str
    title_fr: str
    topic_de: str | None
    topic_en: str | None
    topic_fr: str | None
    source_de: str | None
    source_en: str | None
    source_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None
    url_text_de: str | None
    url_text_en: str | None
    url_text_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'hero_2022'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'img':              get_url(obj, 'img'),
            'img_size':         get_size(obj, 'img'),
            'video':            get_url(obj, 'video'),
            'video_size':       get_size(obj, 'video'),
            'overlay':          obj.attr('overlay'),
            'img_alt_de':       get_attr(obj, 'img_alt', 'ger'),
            'img_alt_en':       get_attr(obj, 'img_alt', 'eng'),
            'img_alt_fr':       get_attr(obj, 'img_alt', 'fra'),
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'topic_de':         get_attr(obj, 'topic', 'ger'),
            'topic_en':         get_attr(obj, 'topic', 'eng'),
            'topic_fr':         get_attr(obj, 'topic', 'fra'),
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'source_de':        get_attr(obj, 'source', 'ger'),
            'source_en':        get_attr(obj, 'source', 'eng'),
            'source_fr':        get_attr(obj, 'source', 'fra'),
            'url_de':           get_url(obj, 'url', 'ger'),
            'url_en':           get_url(obj, 'url', 'eng'),
            'url_fr':           get_url(obj, 'url', 'fra'),
            'url_text_de':      get_attr(obj, 'url_text', 'ger'),
            'url_text_en':      get_attr(obj, 'url_text', 'eng'),
            'url_text_fr':      get_attr(obj, 'url_text', 'fra'),
        }
        return cls.model_validate(mapping)
