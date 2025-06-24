from sqlmodel import Field, Column, DateTime
from datetime import date

from ...zmsfoundation.sqlmodels import ZMSBase


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
    def get_zms_metaid():
        return 'UniaktuellArticle'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'publish_dt_de':    'publishdate_ger',
            'publish_dt_en':    'publishdate_eng',
            'publish_dt_fr':    'publishdate_fra',
            'abstract_de':      'attr_dc_description_ger',
            'abstract_en':      'attr_dc_description_eng',
            'abstract_fr':      'attr_dc_description_fra',
            'category_de':      'rubrik_ger',
            'category_en':      'rubrik_eng',
            'category_fr':      'rubrik_fra',
            'topics_de':        'themen_ger',
            'topics_en':        'themen_eng',
            'topics_fr':        'themen_fra',
            'img_de':           'article_teaserbild_ger',
            'img_en':           'article_teaserbild_eng',
            'img_fr':           'article_teaserbild_fra',
            'url_de':           'obj.getHref2IndexHtmlInContext()',
            'url_en':           'obj.getHref2IndexHtmlInContext()',
            'url_fr':           'obj.getHref2IndexHtmlInContext()',
        }
