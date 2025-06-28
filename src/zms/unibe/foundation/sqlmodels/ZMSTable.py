from .ZMSBase import ZMSBase


class ZMSTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    caption_de: str | None
    caption_en: str | None
    caption_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSTable'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'caption_de':          'caption_ger',
            'caption_en':          'caption_eng',
            'caption_fr':          'caption_fra',
            'descr_de':            'attr_dc_description_ger',
            'descr_en':            'attr_dc_description_eng',
            'descr_fr':            'attr_dc_description_fra',
        }