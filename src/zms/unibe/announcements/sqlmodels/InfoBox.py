from ...foundation.sqlmodels import ZMSBase


class InfoBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    anchor: str | None
    img: str | None
    img_attrs_spec: str | None
    copyright_de: str | None
    copyright_en: str | None
    copyright_fr: str | None
    layout: str | None

    @staticmethod
    def get_zms_metaid():
        return 'infobox'

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
            'anchor':           'ankername',
            'img':              'img',
            'img_attrs_spec':   'img_attrs_spec',
            'copyright_de':     'captionaddon_ger',   
            'copyright_en':     'captionaddon_eng',   
            'copyright_fr':     'captionaddon_fra',
            'layout':           'attr_dc_type_layout',
        }