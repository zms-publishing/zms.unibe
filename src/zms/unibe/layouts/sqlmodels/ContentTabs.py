from ...foundation.sqlmodels import ZMSBase


class ContentTabs(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    layout: str | None
    orientation: str | None

    @staticmethod
    def get_zms_metaid():
        return 'contenttabs'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'layout':           'attr_dc_type_layout',
            'orientation':      'orientation',
        }
