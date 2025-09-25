from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr


class CodeBlock(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    code_de: str | None
    code_en: str | None
    code_fr: str | None
    render_as_newscontainer_de: bool
    render_as_newscontainer_en: bool
    render_as_newscontainer_fr: bool

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'codeblock'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr                      # zms_attr
            'code_de':                      get_attr(obj, 'text', 'ger', dt_exec=False),
            'code_en':                      get_attr(obj, 'text', 'eng', dt_exec=False),
            'code_fr':                      get_attr(obj, 'text', 'fra', dt_exec=False),
            'render_as_newscontainer_de':   get_attr(obj, 'render_as_newscontainer', 'ger'),
            'render_as_newscontainer_en':   get_attr(obj, 'render_as_newscontainer', 'eng'),
            'render_as_newscontainer_fr':   get_attr(obj, 'render_as_newscontainer', 'fra'),
        }
        return cls.model_validate(mapping)
