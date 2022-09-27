from sqlmodel import Field, Column, DateTime
from datetime import datetime

from .zmsdefaults import ZMSBase


class Newsbox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str | None
    start_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    topic: str | None
    url: str | None

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
            'start_dt':         'attr_event_start',
            'topic':            'attr_dc_subject_topic',
            'url':              'attr_url'
        }


class TeaserElement2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str | None
    start_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    end_dt: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))
    topic: str | None
    url: str | None

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
            'topic':            'topic',
            'url':              'url'
        }
