from .ZMSBase import ZMSBase


class ZMSTextarea(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    format: str
    layout: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSTextarea'}

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'format':           'format',
            'layout':           'attr_dc_type_layout',
        }
