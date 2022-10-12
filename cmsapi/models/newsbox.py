from sqlmodel import Field, Column, DateTime
from datetime import datetime

from .zmsobjects import ZMSBase


class Newsbox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str | None
    img: str | None
    start_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    topic_de: str | None
    topic_en: str | None
    topic_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'newsbox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
            'type':             'boxtype',
            'img':              'img',
            'start_dt':         'attr_event_start',
            'text_de':          'text',
            'text_en':          'text',
            'text_fr':          'text',
            'topic_de':         'attr_dc_subject_topic',
            'topic_en':         'attr_dc_subject_topic',
            'topic_fr':         'attr_dc_subject_topic',
            'url_de':           'attr_url',
            'url_en':           'attr_url',
            'url_fr':           'attr_url',
        }
