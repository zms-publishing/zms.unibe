from datetime import datetime

from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_children_count, get_size, get_url, local_timezone
from ...utils.types import OptionalUTCNow


class UniBEEvent(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    teaser_de: str | None
    teaser_en: str | None
    teaser_fr: str | None
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    img_size_de: int | None
    img_size_en: int | None
    img_size_fr: int | None
    start_datetime: OptionalUTCNow
    end_datetime: OptionalUTCNow
    elements: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'UniBEEvent'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'teaser_de':        get_attr(obj, 'eventTeaser', 'ger'),
            'teaser_en':        get_attr(obj, 'eventTeaser', 'eng'),
            'teaser_fr':        get_attr(obj, 'eventTeaser', 'fra'),
            'img_de':           get_url(obj, 'eventBild', 'ger'),
            'img_en':           get_url(obj, 'eventBild', 'eng'),
            'img_fr':           get_url(obj, 'eventBild', 'fra'),
            'img_size_de':      get_size(obj, 'eventBild', 'ger'),
            'img_size_en':      get_size(obj, 'eventBild', 'eng'),
            'img_size_fr':      get_size(obj, 'eventBild', 'fra'),
            'start_datetime': local_timezone(
                datetime.combine(
                    local_timezone(obj.attr('eventStart')).date(),
                    local_timezone(obj.attr('eventStarttime')).time())),
            'end_datetime': local_timezone(
                datetime.combine(
                    local_timezone(obj.attr('eventEnd')).date(),
                    local_timezone(obj.attr('eventEndtime')).time())),
            'elements':         get_children_count(obj),
        }
        return cls.model_validate(mapping)
