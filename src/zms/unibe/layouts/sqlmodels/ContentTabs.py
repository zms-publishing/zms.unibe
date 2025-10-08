from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase


class ContentTabs(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    layout: str | None
    orientation: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'contenttabs'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'layout':           obj.attr('attr_dc_type_layout'),
            'orientation':      obj.attr('orientation'),
        }
        return cls.model_validate(mapping)
