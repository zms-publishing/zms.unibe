from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url


class InfoBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    anchor: str | None
    img: str | None
    img_attrs_spec: str | None
    copyright_de: str | None
    copyright_en: str | None
    copyright_fr: str | None
    layout: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'infobox'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'anchor':           obj.attr('ankername'),
            'img':              get_url(obj, 'img'),
            'img_attrs_spec':   obj.attr('img_attrs_spec'),
            'copyright_de':     get_attr(obj, 'captionaddon', 'ger'),   
            'copyright_en':     get_attr(obj, 'captionaddon', 'eng'),   
            'copyright_fr':     get_attr(obj, 'captionaddon', 'fra'),
            'layout':           obj.attr('attr_dc_type_layout'),
        }
        return cls.model_validate(mapping)
