from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Column, DateTime

from ...foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, parse_datetime, get_url, get_parent_node_uuid


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

    container_uuid: UUID = Field(foreign_key="teasercontainer2022.uuid", ondelete="CASCADE")

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'teaser_element_2022'}

    @classmethod
    def from_zms_obj(cls, obj):
        dict = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'type':             obj.attr('teaser_type'),
            'start_dt':         parse_datetime(obj.attr('event_date_start')),
            'end_dt':           parse_datetime(obj.attr('event_date_end')),
            'location':         obj.attr('event_location'),

            'url_de':           get_url(obj, 'url', 'ger'),
            'url_en':           get_url(obj, 'url', 'eng'),
            'url_fr':           get_url(obj, 'url', 'fra'),
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'topic_de':         get_attr(obj, 'topic', 'ger'),
            'topic_en':         get_attr(obj, 'topic', 'eng'),
            'topic_fr':         get_attr(obj, 'topic', 'fra'),
            'source_de':        get_attr(obj, 'source', 'ger'),
            'source_en':        get_attr(obj, 'source', 'eng'),
            'source_fr':        get_attr(obj, 'source', 'fra'),

            'img_de':           get_url(obj, 'img', 'ger'),
            'img_en':           get_url(obj, 'img', 'eng'),
            'img_fr':           get_url(obj, 'img', 'fra'),
            'img_alt_de':       get_attr(obj, 'img_alt', 'ger'),
            'img_alt_en':       get_attr(obj, 'img_alt', 'eng'),
            'img_alt_fr':       get_attr(obj, 'img_alt', 'fra'),
            
            'container_uuid':   get_parent_node_uuid(obj),
        }
        return cls.model_validate(dict)
