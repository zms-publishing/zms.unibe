from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_url, local_timezone
from ...utils.types import OptionalUTCNow

class MediaNews(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=media_news&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    publish_dt_de: OptionalUTCNow
    publish_dt_en: OptionalUTCNow
    publish_dt_fr: OptionalUTCNow
    abstract_de: str | None
    abstract_en: str | None
    abstract_fr: str | None
    topics_de: str | None
    topics_en: str | None
    topics_fr: str | None
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {
            'path': '/unibe/portal/media_relations/content',
            'meta_id': 'media_news'
        }

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'publish_dt_de':    local_timezone(
                local_timezone(get_attr(obj, 'media_date', 'ger')).date()),
            'publish_dt_en':    local_timezone(
                local_timezone(get_attr(obj, 'media_date', 'eng')).date()),
            'publish_dt_fr':    local_timezone(
                local_timezone(get_attr(obj, 'media_date', 'fra')).date()),
            'abstract_de':      get_attr(obj, 'media_lead', 'ger'),
            'abstract_en':      get_attr(obj, 'media_lead', 'eng'),
            'abstract_fr':      get_attr(obj, 'media_lead', 'fra'),
            'topics_de':        get_attr(obj, 'attr_schlagworte', 'ger'),
            'topics_en':        get_attr(obj, 'attr_schlagworte', 'eng'),
            'topics_fr':        get_attr(obj, 'attr_schlagworte', 'fra'),
            'img_de':           get_url(obj, 'teaser_image', 'ger'),
            'img_en':           get_url(obj, 'teaser_image', 'eng'),
            'img_fr':           get_url(obj, 'teaser_image', 'fra'),
            'url_de':           get_url(obj, None, 'ger'),
            'url_en':           get_url(obj, None, 'eng'),
            'url_fr':           get_url(obj, None, 'fra'),
        }
        return cls.model_validate(mapping)
