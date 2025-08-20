from ...foundation.sqlmodels.ZMSBase import ZMSBase


class Person(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    lastname: str | None
    firstname: str | None
    honorificSuffix: str | None
    position_de: str | None
    position_en: str | None
    position_fr: str | None
    department_de: str | None
    department_en: str | None
    department_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'person'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'lastname':         'lastname',
            'firstname':        'firstname',
            'honorificSuffix':  'honorificSuffix',
            'position_de':      'position_ger',
            'position_en':      'position_eng',
            'position_fr':      'position_fra',
            'department_de':    'department_ger',
            'department_en':    'department_eng',
            'department_fr':    'department_fra',
        }
