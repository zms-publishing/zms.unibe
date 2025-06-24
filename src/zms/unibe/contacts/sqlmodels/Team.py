from ...zmsfoundation.sqlmodels import ZMSBase


class Team(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    sections: int

    @staticmethod
    def get_zms_metaid():
        return 'team'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'sections':         'obj.getObjChildren(teamsection)',
        }
