from sqlmodel import Field, Column, DateTime
from datetime import date

from .zmsobjects import ZMSBase


class MediaRelease(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=media_news&types=%2A
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
    def get_zms_metaid():
        return 'media_news'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'publish_dt_de':    'media_date_ger',
            'publish_dt_en':    'media_date_eng',
            'publish_dt_fr':    'media_date_fra',
            'abstract_de':      'media_lead_ger',
            'abstract_en':      'media_lead_eng',
            'abstract_fr':      'media_lead_fra',
            'topics_de':        'attr_schlagworte_ger',
            'topics_en':        'attr_schlagworte_eng',
            'topics_fr':        'attr_schlagworte_fra',
            'img_de':           'teaser_image_ger',
            'img_en':           'teaser_image_eng',
            'img_fr':           'teaser_image_fra',
            'url_de':           'obj.getHref2IndexHtmlInContext()',
            'url_en':           'obj.getHref2IndexHtmlInContext()',
            'url_fr':           'obj.getHref2IndexHtmlInContext()',
        }
