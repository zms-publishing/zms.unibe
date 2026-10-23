from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import flatten_to_str_list, normalize_split_by
from ...utils.helpers import get_attr, get_size, get_url
from ...utils.types import PostgreSQLArray


class Hero2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img: str | None = None
    img_size: int | None = None
    video: str | None = None
    video_size: int | None = None
    overlay: bool
    img_alt_de: str | None = None
    img_alt_en: str | None = None
    img_alt_fr: str | None = None
    title_de: str
    title_en: str
    title_fr: str
    topic_de: PostgreSQLArray
    topic_en: PostgreSQLArray
    topic_fr: PostgreSQLArray
    source_de: str | None = None
    source_en: str | None = None
    source_fr: str | None = None
    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None
    url_text_de: str | None = None
    url_text_en: str | None = None
    url_text_fr: str | None = None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'hero_2022'}

    @classmethod
    def from_zms_obj(cls, obj):
        
        topic_de = flatten_to_str_list(normalize_split_by(
            get_attr(obj, 'topic', 'ger')))
        topic_en = flatten_to_str_list(normalize_split_by(
            get_attr(obj, 'topic', 'eng')))
        topic_fr = flatten_to_str_list(normalize_split_by(
            get_attr(obj, 'topic', 'fra')))
        
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
            'topic_de':         topic_de,
            'topic_en':         topic_en,
            'topic_fr':         topic_fr,
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
