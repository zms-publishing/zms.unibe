from ...foundation.sqlmodels import ZMSBase


class Hero2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img: str | None
    img_size: str | None
    video: str | None
    video_size: int | None
    overlay: bool
    img_alt_de: str | None
    img_alt_en: str | None
    img_alt_fr: str | None
    title_de: str
    title_en: str
    title_fr: str
    topic_de: str | None
    topic_en: str | None
    topic_fr: str | None
    source_de: str | None
    source_en: str | None
    source_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None
    url_text_de: str | None
    url_text_en: str | None
    url_text_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'hero_2022'}

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'img':              'img',
            'img_size':         'img',
            'video':            'video',
            'video_size':       'video',
            'overlay':          'overlay',
            'img_alt_de':       'img_alt_ger',
            'img_alt_en':       'img_alt_eng',
            'img_alt_fr':       'img_alt_fra',
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'topic_de':         'topic_ger',
            'topic_en':         'topic_eng',
            'topic_fr':         'topic_fra',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'source_de':        'source_ger',
            'source_en':        'source_eng',
            'source_fr':        'source_fra',
            'url_de':           'url_ger',
            'url_en':           'url_eng',
            'url_fr':           'url_fra',
            'url_text_de':      'url_text_ger',
            'url_text_en':      'url_text_eng',
            'url_text_fr':      'url_text_fra',
        }
