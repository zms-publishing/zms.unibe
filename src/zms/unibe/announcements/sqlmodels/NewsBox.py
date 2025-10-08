from datetime import datetime
from uuid import UUID
from sqlmodel import Field, Column, DateTime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, parse_datetime, get_parent_node_uuid


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
    container_uuid: UUID = Field(foreign_key="newscontainer.uuid", ondelete="CASCADE")

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'newsbox'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'type':             obj.attr('boxtype'),
            'img':              get_url(obj, 'img'),
            'start_dt':         parse_datetime(obj.attr('attr_event_start')),
            'end_dt':           parse_datetime(obj.attr('ttr_event_end')),
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'topic_de':         get_attr(obj, 'attr_dc_subject_topic', 'ger'),
            'topic_en':         get_attr(obj, 'attr_dc_subject_topic', 'eng'),
            'topic_fr':         get_attr(obj, 'attr_dc_subject_topic', 'fra'),
            'url_de':           get_url(obj, 'attr_url', 'ger'),
            'url_en':           get_url(obj, 'attr_url', 'eng'),
            'url_fr':           get_url(obj, 'attr_url', 'fra'),
            'container_uuid':   get_parent_node_uuid(obj),
        }
        return cls.model_validate(mapping)
