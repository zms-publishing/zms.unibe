from uuid import UUID
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url, get_parent_node_uuid, get_parent_node_attr


class ServiceLink(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    meta_id: str
    title_de: str
    title_en: str
    title_fr: str
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    keywords_de: str | None
    keywords_en: str | None
    keywords_fr: str | None
    href_de: str | None
    href_en: str | None
    href_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None
    parent_uuid: UUID
    parent_title_de: str
    parent_title_en: str
    parent_title_fr: str

    @staticmethod
    def get_zms_catalog_query():
        return {'path': '/unibe/uniapp/content/'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'meta_id':          obj.attr('meta_id'),
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'keywords_de':      get_attr(obj, 'attr_dc_description', 'ger'),
            'keywords_en':      get_attr(obj, 'attr_dc_description', 'eng'),
            'keywords_fr':      get_attr(obj, 'attr_dc_description', 'fra'),
            'href_de':          get_url(obj, 'attr_ref', 'ger'),
            'href_en':          get_url(obj, 'attr_ref', 'eng'),
            'href_fr':          get_url(obj, 'attr_ref', 'fra'),
            'url_de':           get_url(obj, 'file', 'ger'),
            'url_en':           get_url(obj, 'file', 'eng'),
            'url_fr':           get_url(obj, 'file', 'fra'),
            'parent_uuid':      get_parent_node_uuid(obj),
            'parent_title_de':  get_parent_node_attr(obj, 'title', 'ger'),
            'parent_title_en':  get_parent_node_attr(obj, 'title', 'eng'),
            'parent_title_fr':  get_parent_node_attr(obj, 'title', 'fra'),
        }
        return cls.model_validate(mapping)
