from datetime import datetime

from sqlmodel import Field, Column, Date, Time

from ...foundation.sqlmodels import ZMSBase


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
    start_at_date: datetime | None = Field(sa_column=Column(Date(), nullable=True))
    start_at_time: datetime | None = Field(sa_column=Column(Time(timezone=False), nullable=True))
    end_at_date: datetime | None = Field(sa_column=Column(Date(), nullable=True))
    end_at_time: datetime | None = Field(sa_column=Column(Time(timezone=False), nullable=True))
    elements: int

    @staticmethod
    def get_zms_metaid():
        return 'UniBEEvent'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'teaser_de':        'eventTeaser_ger',
            'teaser_en':        'eventTeaser_eng',
            'teaser_fr':        'eventTeaser_fra',
            'img_de':           'eventBild_ger',
            'img_en':           'eventBild_eng',
            'img_fr':           'eventBild_fra',
            'img_size_de':      'eventBild_ger',
            'img_size_en':      'eventBild_eng',
            'img_size_fr':      'eventBild_fra',
            'start_at_date':    'eventStart',
            'start_at_time':    'eventStarttime',
            'end_at_date':      'eventEnd',
            'end_at_time':      'eventEndtime',
            'elements':         'obj.getObjChildren(e)',
        }
