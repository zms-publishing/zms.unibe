from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr


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
    def get_zms_catalog_query():
        return {'meta_id': 'person'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'lastname':         obj.attr('lastname'),
            'firstname':        obj.attr('firstname'),
            'honorificSuffix':  obj.attr('honorificSuffix'),
            'position_de':      get_attr(obj, 'position', 'ger'),
            'position_en':      get_attr(obj, 'position', 'eng'),
            'position_fr':      get_attr(obj, 'position', 'fra'),
            'department_de':    get_attr(obj, 'department', 'ger'),
            'department_en':    get_attr(obj, 'department', 'eng'),
            'department_fr':    get_attr(obj, 'department', 'fra'),
        }
        return cls.model_validate(mapping)
