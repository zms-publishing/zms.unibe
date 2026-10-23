from uuid import UUID

from sqlmodel import Field

from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_parent_node_uuid, get_url, local_timezone
from ...utils.types import OptionalDateTime


class NewsBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str | None = None
    img: str | None = None
    start_dt: OptionalDateTime
    end_dt: OptionalDateTime
    text_de: str | None = None
    text_en: str | None = None
    text_fr: str | None = None
    topic_de: str | None = None
    topic_en: str | None = None
    topic_fr: str | None = None
    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None
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
            'start_dt':         local_timezone(obj.attr('attr_event_start')),
            'end_dt':           local_timezone(obj.attr('attr_event_end')),
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
