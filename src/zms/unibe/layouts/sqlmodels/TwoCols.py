from ...foundation.sqlmodels.ZMSBase import ZMSBase


class TwoCols(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'twocols'}

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
        }