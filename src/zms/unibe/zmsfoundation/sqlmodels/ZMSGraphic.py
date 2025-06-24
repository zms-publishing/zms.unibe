from ZMSBase import ZMSBase


class ZMSGraphic(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    imghires_de: str | None
    imghires_en: str | None
    imghires_fr: str | None
    imgsuperres_de: str | None
    imgsuperres_en: str | None
    imgsuperres_fr: str | None
    img_size_de: int | None
    img_size_en: int | None
    img_size_fr: int | None
    imghires_size_de: int | None
    imghires_size_en: int | None
    imghires_size_fr: int | None
    imgsuperres_size_de: int | None
    imgsuperres_size_en: int | None
    imgsuperres_size_fr: int | None
    img_attrs_spec: str | None
    attr_url_de: str | None
    attr_url_en: str | None
    attr_url_fr: str | None
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    captionaddon_de: str | None
    captionaddon_en: str | None
    captionaddon_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSGraphic'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr

            'descr_de': 'attr_dc_description_ger',
            'descr_en': 'attr_dc_description_eng',
            'descr_fr': 'attr_dc_description_fra',
            'img_de': 'img_ger',
            'img_en': 'img_eng',
            'img_fr': 'img_fra',
            'imghires_de': 'imghires_ger',
            'imghires_en': 'imghires_eng',
            'imghires_fr': 'imghires_fra',
            'imgsuperres_de': 'imgsuperres_ger',
            'imgsuperres_en': 'imgsuperres_eng',
            'imgsuperres_fr': 'imgsuperres_fra',
            'img_size_de': 'img_ger',
            'img_size_en': 'img_eng',
            'img_size_fr': 'img_fra',
            'imghires_size_de': 'imghires_ger',
            'imghires_size_en': 'imghires_eng',
            'imghires_size_fr': 'imghires_fra',
            'imgsuperres_size_de': 'imgsuperres_ger',
            'imgsuperres_size_en': 'imgsuperres_eng',
            'imgsuperres_size_fr': 'imgsuperres_fra',
            'img_attrs_spec': 'img_attrs_spec',
            'attr_url_de': 'attr_url_ger',
            'attr_url_en': 'attr_url_eng',
            'attr_url_fr': 'attr_url_fra',
            'text_de': 'text_ger',
            'text_en': 'text_eng',
            'text_fr': 'text_fra',
            'captionaddon_de': 'captionaddon_ger',
            'captionaddon_en': 'captionaddon_eng',
            'captionaddon_fr': 'captionaddon_fra',
        }
