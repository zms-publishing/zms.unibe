from ...zmsfoundation.sqlmodels import ZMSBase


class ZMSFormulator(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    items: int | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFormulator'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'items':            'obj.getObjChildren(formulatorItems)',
        }
