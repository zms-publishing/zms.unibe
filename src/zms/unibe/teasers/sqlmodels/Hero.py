from ...zmsfoundation.sqlmodels import ZMSBase


class Hero(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img: str | None
    img_size: int | None
    name_de: str
    name_en: str
    name_fr: str
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    quote_de: str | None
    quote_en: str | None
    quote_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None
    url_type_de: str | None
    url_type_en: str | None
    url_type_fr: str | None
    url_title_de: str | None
    url_title_en: str | None
    url_title_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'hero'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'img':              'hero_image',
            'img_size':         'hero_image',
            'name_de':          'hero_name_ger',
            'name_en':          'hero_name_eng',
            'name_fr':          'hero_name_fra',
            'title_de':         'hero_title_ger',
            'title_en':         'hero_title_eng',
            'title_fr':         'hero_title_fra',
            'quote_de':         'hero_quote_ger',
            'quote_en':         'hero_quote_eng',
            'quote_fr':         'hero_quote_fra',
            'url_de':           'url_ger',
            'url_en':           'url_eng',
            'url_fr':           'url_fra',
            'url_type_de':      'url_type_ger',
            'url_type_en':      'url_type_eng',
            'url_type_fr':      'url_type_fra',
            'url_title_de':     'url_title_ger',
            'url_title_en':     'url_title_eng',
            'url_title_fr':     'url_title_fra',
        }