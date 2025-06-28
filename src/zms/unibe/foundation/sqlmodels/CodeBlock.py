from .ZMSBase import ZMSBase


class CodeBlock(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    code_de: str | None
    code_en: str | None
    code_fr: str | None
    render_as_newscontainer_de: bool
    render_as_newscontainer_en: bool
    render_as_newscontainer_fr: bool

    @staticmethod
    def get_zms_metaid():
        return 'codeblock'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'code_de':          'obj.getObjAttrValue(text)',
            'code_en':          'obj.getObjAttrValue(text)',
            'code_fr':          'obj.getObjAttrValue(text)',
            'render_as_newscontainer_de': 'render_as_newscontainer_ger',
            'render_as_newscontainer_en': 'render_as_newscontainer_eng',
            'render_as_newscontainer_fr': 'render_as_newscontainer_fra',
        }
