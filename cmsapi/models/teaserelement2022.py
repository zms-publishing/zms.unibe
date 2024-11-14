from sqlmodel import Field, Column, DateTime
from datetime import datetime

from .zmsobjects import ZMSBase

class TeaserContainer2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    layout: str

    @staticmethod
    def get_zms_metaid():
        return 'teaser_container_2022'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'layout':           'layout',
        }


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
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'teaser_type',
            'start_dt':         'event_date_start',
            'end_dt':           'event_date_end',
            'location':         'event_location',

            'url_de':           'url_ger',
            'url_en':           'url_eng',
            'url_fr':           'url_fra',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'topic_de':         'topic_ger',
            'topic_en':         'topic_eng',
            'topic_fr':         'topic_fra',
            'source_de':        'source_ger',
            'source_en':        'source_eng',
            'source_fr':        'source_fra',

            'img_de':           'img_ger',
            'img_en':           'img_eng',
            'img_fr':           'img_fra',
            'img_alt_de':       'img_alt_ger',
            'img_alt_en':       'img_alt_eng',
            'img_alt_fr':       'img_alt_fra',
        }
