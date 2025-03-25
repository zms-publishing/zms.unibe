from sqlmodel import Field, Column, DateTime
from datetime import datetime
from uuid import UUID

from .zmsobjects import ZMSBase


class NewsContainer(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str | None

    @staticmethod
    def get_zms_metaid():
        return 'newscontainer'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'boxtype',
        }


class NewsBox(ZMSBase, table=True):
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
    container_uuid: UUID = Field(foreign_key="newscontainer.uuid")

    @staticmethod
    def get_zms_metaid():
        return 'newsbox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'boxtype',
            'img':              'img',
            'start_dt':         'attr_event_start',
            'end_dt':           'attr_event_end',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'topic_de':         'attr_dc_subject_topic_ger',
            'topic_en':         'attr_dc_subject_topic_eng',
            'topic_fr':         'attr_dc_subject_topic_fra',
            'url_de':           'attr_url_ger',
            'url_en':           'attr_url_eng',
            'url_fr':           'attr_url_fra',
            'container_uuid':   'obj.getParentNode()._uid',
        }
