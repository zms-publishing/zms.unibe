from datetime import date
from sqlmodel import Field, Column, DateTime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, parse_datetime, strip_cmstest


class MediaNews(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=media_news&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    publish_dt_de: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    publish_dt_en: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    publish_dt_fr: date | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
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
            'publish_dt_de':    parse_datetime(get_attr(obj, 'media_date', 'ger')),
            'publish_dt_en':    parse_datetime(get_attr(obj, 'media_date', 'eng')),
            'publish_dt_fr':    parse_datetime(get_attr(obj, 'media_date', 'fra')),
            'abstract_de':      get_attr(obj, 'media_lead', 'ger'),
            'abstract_en':      get_attr(obj, 'media_lead', 'eng'),
            'abstract_fr':      get_attr(obj, 'media_lead', 'fra'),
            'topics_de':        get_attr(obj, 'attr_schlagworte', 'ger'),
            'topics_en':        get_attr(obj, 'attr_schlagworte', 'eng'),
            'topics_fr':        get_attr(obj, 'attr_schlagworte', 'fra'),
            'img_de':           get_url(obj, 'teaser_image', 'ger'),
            'img_en':           get_url(obj, 'teaser_image', 'eng'),
            'img_fr':           get_url(obj, 'teaser_image', 'fra'),
            'url_de':           strip_cmstest(obj.getHref2IndexHtmlInContext(context=None)),  # TODO: check -> REQUEST?
            'url_en':           strip_cmstest(obj.getHref2IndexHtmlInContext(context=None)),  # TODO: check -> REQUEST?
            'url_fr':           strip_cmstest(obj.getHref2IndexHtmlInContext(context=None)),  # TODO: check -> REQUEST?
        }
        return cls.model_validate(mapping)
