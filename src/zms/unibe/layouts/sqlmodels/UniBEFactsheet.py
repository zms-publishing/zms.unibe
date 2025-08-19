from ...foundation.sqlmodels.ZMSBase import ZMSBase


class UniBEFactsheet(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    titleimg_de: str | None
    titleimg_en: str | None
    titleimg_fr: str | None
    titleimg_size_de: str | None
    titleimg_size_en: str | None
    titleimg_size_fr: str | None
    elements: int

    @staticmethod
    def get_zms_metaid():
        return 'UniBEFactsheet'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'titleimg_de':      'titleimage_ger',
            'titleimg_en':      'titleimage_eng',
            'titleimg_fr':      'titleimage_fra',
            'titleimg_size_de': 'titleimage_ger',
            'titleimg_size_en': 'titleimage_eng',
            'titleimg_size_fr': 'titleimage_fra',
            'elements':         'obj.getObjChildren(e)',
        }
