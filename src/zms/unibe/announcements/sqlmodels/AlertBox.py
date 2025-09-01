from ...foundation.sqlmodels.ZMSBase import ZMSBase


class AlertBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    type: str | None
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'alertbox'}

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'type':             'alerttype',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'url_de':           'attr_url_ger',
            'url_en':           'attr_url_eng',
            'url_fr':           'attr_url_fra',
        }
