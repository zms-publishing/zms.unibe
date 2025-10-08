from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_children_count

class Team(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    sections: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'team'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'sections':         get_children_count(obj, 'teamsection'),
        }
        return cls.model_validate(mapping)
