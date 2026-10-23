from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_url, local_timezone
from ...utils.types import OptionalDateTime, PostgreSQLArray


class UniaktuellArticle(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=UniaktuellArticle&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    publish_dt_de: OptionalDateTime
    publish_dt_en: OptionalDateTime
    publish_dt_fr: OptionalDateTime
    abstract_de: str | None = None
    abstract_en: str | None = None
    abstract_fr: str | None = None
    category_de: PostgreSQLArray
    category_en: PostgreSQLArray
    category_fr: PostgreSQLArray
    topics_de: str | None = None
    topics_en: str | None = None
    topics_fr: str | None = None
    img_de: str | None = None
    img_en: str | None = None
    img_fr: str | None = None
    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None

    @staticmethod
    def get_zms_catalog_query():
        return {
            'path': '/unibe/portal/uni_aktuell/content',
            'meta_id': 'UniaktuellArticle'
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
                local_timezone(get_attr(obj, 'publishdate', 'ger')).date()),
            'publish_dt_en':    local_timezone(
                local_timezone(get_attr(obj, 'publishdate', 'eng')).date()),
            'publish_dt_fr':    local_timezone(
                local_timezone(get_attr(obj, 'publishdate', 'fra')).date()),
            'abstract_de':      get_attr(obj, 'attr_dc_description', 'ger'),
            'abstract_en':      get_attr(obj, 'attr_dc_description', 'eng'),
            'abstract_fr':      get_attr(obj, 'attr_dc_description', 'fra'),
            'category_de':      get_attr(obj, 'rubrik', 'ger'),
            'category_en':      get_attr(obj, 'rubrik', 'eng'),
            'category_fr':      get_attr(obj, 'rubrik', 'fra'),
            'topics_de':        get_attr(obj, 'themen', 'ger'),
            'topics_en':        get_attr(obj, 'themen', 'eng'),
            'topics_fr':        get_attr(obj, 'themen', 'fra'),
            'img_de':           get_url(obj, 'article_teaserbild', 'ger'),
            'img_en':           get_url(obj, 'article_teaserbild', 'eng'),
            'img_fr':           get_url(obj, 'article_teaserbild', 'fra'),
            'url_de':           get_url(obj, None, 'ger'),
            'url_en':           get_url(obj, None, 'eng'),
            'url_fr':           get_url(obj, None, 'fra'),
        }
        return cls.model_validate(mapping)
