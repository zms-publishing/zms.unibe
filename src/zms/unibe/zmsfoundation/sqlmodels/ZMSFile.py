from ZMSBase import ZMSBase


class ZMSFile(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    file_de: str | None
    file_en: str | None
    file_fr: str | None
    file_size_de: int | None
    file_size_en: int | None
    file_size_fr: int | None
    filetype: str
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    amount_de: str | None
    amount_en: str | None
    amount_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFile'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'file_de':          'file_ger',
            'file_en':          'file_eng',
            'file_fr':          'file_fra',
            'file_size_de':     'file_ger',
            'file_size_en':     'file_eng',
            'file_size_fr':     'file_fra', 
            'filetype':         'filetype',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'amount_de':        'amount_ger',
            'amount_en':        'amount_eng',
            'amount_fr':        'amount_fra',
        }
