from datetime import date
from sqlmodel import Field, Column, DateTime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url


class UniaktuellArticle(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=UniaktuellArticle&types=%2A
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
    category_de: str | None
    category_en: str | None
    category_fr: str | None
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
            'publish_dt_de':    get_attr(obj, 'publishdate', 'ger'),
            'publish_dt_en':    get_attr(obj, 'publishdate', 'eng'),
            'publish_dt_fr':    get_attr(obj, 'publishdate', 'fra'),
            'abstract_de':      get_attr(obj, 'attr_dc_description', 'ger'),
            'abstract_en':      get_attr(obj, 'attr_dc_description', 'eng'),
            'abstract_fr':      get_attr(obj, 'attr_dc_description', 'fra'),
            'category_de':      get_attr(obj, 'rubrik', 'ger'),
            'category_en':      get_attr(obj, 'rubrik', 'eng'),
            'category_fr':      get_attr(obj, 'rubrik', 'fra'),
            'topics_de':        get_attr(obj, 'themen', 'ger'),
            'topics_en':        get_attr(obj, 'themen', 'eng'),
            'topics_fr':        get_attr(obj, 'themen', 'fra'),
            'img_de':           get_attr(obj, 'article_teaserbild', 'ger'),
            'img_en':           get_attr(obj, 'article_teaserbild', 'eng'),
            'img_fr':           get_attr(obj, 'article_teaserbild', 'fra'),
            'url_de':           get_url(obj, None, 'ger', obj_context_href=True),
            'url_en':           get_url(obj, None, 'eng', obj_context_href=True),
            'url_fr':           get_url(obj, None, 'fra', obj_context_href=True),
        }
        return cls.model_validate(mapping)
