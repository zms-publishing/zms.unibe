from ZMSBase import ZMSBase


class ZMSDocument(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDocument'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'attr_dc_type',
        }
