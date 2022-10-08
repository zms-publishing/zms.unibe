from sqlmodel import Field, Column, DateTime
from datetime import datetime

from .zmsobjects import ZMSBase


class TeaserElement2022(ZMSBase, table=True):  # http://localhost:5003/v3/zms/models?metaobj=teaser_element_2022&types=%2A
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str
    start_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    location: str | None

    url_de: str | None
    url_en: str | None
    url_fr: str | None
    text_de: str
    text_en: str
    text_fr: str
    topic_de: str | None
    topic_en: str | None
    topic_fr: str | None
    source_de: str | None
    source_en: str | None
    source_fr: str | None

    img_de: str | None
    img_en: str | None
    img_fr: str | None
    img_alt_de: str | None
    img_alt_en: str | None
    img_alt_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'teaser_element_2022'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
            'type':             'teaser_type',
            'start_dt':         'event_date_start',
            'end_dt':           'event_date_end',
            'location':         'event_location',

            'url_de':           'url',
            'url_en':           'url',
            'url_fr':           'url',
            'text_de':          'text',
            'text_en':          'text',
            'text_fr':          'text',
            'topic_de':         'topic',
            'topic_en':         'topic',
            'topic_fr':         'topic',
            'source_de':        'source',
            'source_en':        'source',
            'source_fr':        'source',

            'img_de':           'img',
            'img_en':           'img',
            'img_fr':           'img',
            'img_alt_de':       'img_alt',
            'img_alt_en':       'img_alt',
            'img_alt_fr':       'img_alt',
        }
