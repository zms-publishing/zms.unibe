from ...zmsfoundation.sqlmodels import ZMSBase


class ContactBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    titlealt_de: str | None
    titlealt_en: str | None
    titlealt_fr: str | None
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    sections: int

    @staticmethod
    def get_zms_metaid():
        return 'contactbox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'titlealt_de':      'titlealt_ger',
            'titlealt_en':      'titlealt_eng',
            'titlealt_fr':      'titlealt_fra',
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'sections':         'obj.getObjChildren(sections)',
        }
