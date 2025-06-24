from ...zmsfoundation.sqlmodels import ZMSBase


class TeaserContainer2022(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    layout: str

    @staticmethod
    def get_zms_metaid():
        return 'teaser_container_2022'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'layout':           'layout',
        }
