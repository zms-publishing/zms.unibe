from sqlmodel import SQLModel, Field, Column, DateTime, Date, Time, JSON
#from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import UUID


class ZMSBase(SQLModel, table=False):  # Base class from which ZMSObjects inherit
    uuid: UUID = Field(primary_key=True)
    site_uuid: UUID = Field(foreign_key="zmssite.uuid", ondelete="CASCADE")
    active_de: bool
    active_en: bool
    active_fr: bool
    active_start_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_start_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_start_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    active_end_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    created_dt_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_de: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_en: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    lastmod_dt_fr: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)
    sort_id_parent: int
    sort_id: int
    level: int
    path: str

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'uuid':             'obj._uid',
            'site_uuid':        'obj.getDocumentElement()._uid',
            'active_de':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_en':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_fr':        'obj.isActivatedByCheckboxAndTimeline()',
            'active_start_de':  'attr_active_start_ger',
            'active_start_en':  'attr_active_start_eng',
            'active_start_fr':  'attr_active_start_fra',
            'active_end_de':    'attr_active_end_ger',
            'active_end_en':    'attr_active_end_eng',
            'active_end_fr':    'attr_active_end_fra',
            'created_dt_de':    'created_dt_ger',
            'created_dt_en':    'created_dt_eng',
            'created_dt_fr':    'created_dt_fra',
            'lastmod_dt_de':    'change_dt_ger',
            'lastmod_dt_en':    'change_dt_eng',
            'lastmod_dt_fr':    'change_dt_fra',
            'sort_id_parent':   'obj.getParentNode().getSortId()',
            'sort_id':          'obj.getSortId()',
            'level':            'obj.getLevel()',
            'path':             'obj.getPath()',
        }


class ZMSSite(SQLModel, table=True):  # http://localhost:5003/v3/zms/models?metaobj=ZMS&types=%2A
    __table_args__ = {'extend_existing': True}
    uuid: UUID = Field(primary_key=True)
    active_de: bool
    active_en: bool
    active_fr: bool
    title_de: str
    title_en: str
    title_fr: str
    domain: str | None
    alias: str | None
    level: int
    path: str
    type: str
    theme: str
    count_objs: int
    parent_uuid: UUID

    @staticmethod
    def get_zms_metaid():
        return 'ZMS'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'domain':           'obj.getConfProperty(UniBE.Server)',
            'alias':            'obj.getConfProperty(UniBE.Alias)',
            'level':            'obj.getLevel()',
            'path':             'obj.getPath()',
            'type':             'obj.getType()',
            'theme':            'obj.getConfProperty(ZMS.theme)',
            'count_objs':       'obj.getCount()',
            'parent_uuid':      'obj.getParentHome()._uid'
        }


class ZMSFolder(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFolder'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'attr_dc_type',
        }


class ZMSDocument(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    type: str

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDocument'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'type':             'attr_dc_type',
        }


class ZMSFormulator(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    items: int | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFormulator'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'items':            'obj.getObjChildren(formulatorItems)',
        }


# TODO: ZMSLinkContainer (25)
# TODO: ZMSLinkElement (31.238)


# TODO: linkcontainer (10.022)
# TODO: linkelement (76.096)


class ZMSBoris(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    dataurl: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    boris_data: str | None  # = Field(sa_column=Column(JSONB), default_factory=dict)
    lastupdate: datetime | None = Field(sa_type=DateTime(timezone=True), nullable=True)

    @staticmethod
    def get_zms_metaid():
        return 'ZMSBoris'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'dataurl':          'dataurl',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'boris_data':       'obj.getData(_datafilecached)',
            'lastupdate':       '_datalastupdated',
        }


class ZMSDataTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    datatype: str
    dataremote: bool
    datawebservice: str | None
    dataurl_de: str | None
    dataurl_en: str | None
    dataurl_fr: str | None
    datafile_de: str | None
    datafile_en: str | None
    datafile_fr: str | None
    cached_data_de: str | None
    cached_data_en: str | None
    cached_data_fr: str | None
    upload_data_de: str | None
    upload_data_en: str | None
    upload_data_fr: str | None
    lastupdate: datetime | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSDataTable'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'datatype':         'datatype',
            'dataremote':       'dataremote',
            'datawebservice':   'datawebservice',
            'dataurl_de':       'dataurl_ger',
            'dataurl_en':       'dataurl_eng',
            'dataurl_fr':       'dataurl_fra',
            'datafile_de':      'datafile_ger',
            'datafile_en':      'datafile_eng',
            'datafile_fr':      'datafile_fra',
            'cached_data_de':   'obj.getData(_datafilecached_ger)',
            'cached_data_en':   'obj.getData(_datafilecached_eng)',
            'cached_data_fr':   'obj.getData(_datafilecached_fra)',
            'upload_data_de':   'obj.getData(datafile_ger)',
            'upload_data_en':   'obj.getData(datafile_eng)',
            'upload_data_fr':   'obj.getData(datafile_fra)',
            'lastupdate':       '_datalastupdated',
        }


class ZMSTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    caption_de: str | None
    caption_en: str | None
    caption_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSTable'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'caption_de':          'caption_ger',
            'caption_en':          'caption_eng',
            'caption_fr':          'caption_fra',
            'descr_de':            'attr_dc_description_ger',
            'descr_en':            'attr_dc_description_eng',
            'descr_fr':            'attr_dc_description_fra',
        }


class ZMSGraphic(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    imghires_de: str | None
    imghires_en: str | None
    imghires_fr: str | None
    imgsuperres_de: str | None
    imgsuperres_en: str | None
    imgsuperres_fr: str | None
    img_size_de: int | None
    img_size_en: int | None
    img_size_fr: int | None
    imghires_size_de: int | None
    imghires_size_en: int | None
    imghires_size_fr: int | None
    imgsuperres_size_de: int | None
    imgsuperres_size_en: int | None
    imgsuperres_size_fr: int | None
    img_attrs_spec: str | None
    attr_url_de: str | None
    attr_url_en: str | None
    attr_url_fr: str | None
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    captionaddon_de: str | None
    captionaddon_en: str | None
    captionaddon_fr: str | None
    
    @staticmethod
    def get_zms_metaid():
        return 'ZMSGraphic'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr

            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'img_de':           'img_ger',
            'img_en':           'img_eng',
            'img_fr':           'img_fra',
            'imghires_de':      'imghires_ger',
            'imghires_en':      'imghires_eng',
            'imghires_fr':      'imghires_fra',
            'imgsuperres_de':   'imgsuperres_ger',
            'imgsuperres_en':   'imgsuperres_eng',
            'imgsuperres_fr':   'imgsuperres_fra',
            'img_size_de':      'img_ger',
            'img_size_en':      'img_eng',
            'img_size_fr':      'img_fra',
            'imghires_size_de': 'imghires_ger',
            'imghires_size_en': 'imghires_eng',
            'imghires_size_fr': 'imghires_fra',
            'imgsuperres_size_de': 'imgsuperres_ger',
            'imgsuperres_size_en': 'imgsuperres_eng',
            'imgsuperres_size_fr': 'imgsuperres_fra',
            'img_attrs_spec':   'img_attrs_spec',
            'attr_url_de':      'attr_url_ger',
            'attr_url_en':      'attr_url_eng',
            'attr_url_fr':      'attr_url_fra',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'captionaddon_de':  'captionaddon_ger',
            'captionaddon_en':  'captionaddon_eng',
            'captionaddon_fr':  'captionaddon_fra',
        }


class ZMSFile(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    file_de: str | None
    file_en: str | None
    file_fr: str | None
    file_size_de: int | None
    file_size_en: int | None
    file_size_fr: int | None
    filetype: str
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    amount_de: str | None
    amount_en: str | None
    amount_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'ZMSFile'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'file_de':          'file_ger',
            'file_en':          'file_eng',
            'file_fr':          'file_fra',
            'file_size_de':     'file_ger',
            'file_size_en':     'file_eng',
            'file_size_fr':     'file_fra', 
            'filetype':         'filetype',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'amount_de':        'amount_ger',
            'amount_en':        'amount_eng',
            'amount_fr':        'amount_fra',
        }


class TwoCols(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'twocols'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
        }


class ContentTabs(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    layout: str | None
    orientation: str | None

    @staticmethod
    def get_zms_metaid():
        return 'contenttabs'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'layout':           'attr_dc_type_layout',
            'orientation':      'orientation',
        }


class ContentPane(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    elements: int | None
    contenttabs_uuid: UUID

    @staticmethod
    def get_zms_metaid():
        return 'contentpane'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'elements':         'obj.getObjChildren(e)',
            'contenttabs_uuid': 'obj.getParentNode()._uid',
        }


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
    def get_zms_metaid():
        return 'infobox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'anchor':           'ankername',
            'img':              'img',
            'img_attrs_spec':   'img_attrs_spec',
            'copyright_de':     'captionaddon_ger',   
            'copyright_en':     'captionaddon_eng',   
            'copyright_fr':     'captionaddon_fra',
            'layout':           'attr_dc_type_layout',
        }


class AlertBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    type: str | None
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None

    @staticmethod
    def get_zms_metaid():
        return 'alertbox'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'type':             'alerttype',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'url_de':           'attr_url_ger',
            'url_en':           'attr_url_eng',
            'url_fr':           'attr_url_fra',
        }

    
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


class ContactBoxSection(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    intersection_title_de: str | None
    intersection_title_en: str | None
    intersection_title_fr: str | None
    interpara_title_de: str | None
    interpara_title_en: str | None
    interpara_title_fr: str | None
    contactbox_uuid: UUID

    @staticmethod
    def get_zms_metaid():
        return 'contactboxsection'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'intersection_title_de':      'intersection_title_ger',
            'intersection_title_en':      'intersection_title_eng',
            'intersection_title_fr':      'intersection_title_fra',
            'interpara_title_de':         'interpara_title_ger',
            'interpara_title_en':         'interpara_title_eng',
            'interpara_title_fr':         'interpara_title_fra',
            'contactbox_uuid':            'obj.getParentNode()._uid',
        }


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


class TeamSection(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    team_uuid: UUID | None
    persons: int

    @staticmethod
    def get_zms_metaid():
        return 'teamsection'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'team_uuid':        'obj.getParentNode()._uid',
            'persons':          'obj.getObjChildren(person)',
        }


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


class UniBEFactsheet(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    titleimg_de: str | None
    titleimg_en: str | None
    titleimg_fr: str | None
    titleimg_size_de: str | None
    titleimg_size_en: str | None
    titleimg_size_fr: str | None
    elements: int

    @staticmethod
    def get_zms_metaid():
        return 'UniBEFactsheet'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'titleimg_de':      'titleimage_ger',
            'titleimg_en':      'titleimage_eng',
            'titleimg_fr':      'titleimage_fra',
            'titleimg_size_de': 'titleimage_ger',
            'titleimg_size_en': 'titleimage_eng',
            'titleimg_size_fr': 'titleimage_fra',
            'elements':         'obj.getObjChildren(e)',
        }


class UniBEEvent(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    teaser_de: str | None
    teaser_en: str | None
    teaser_fr: str | None
    img_de: str | None
    img_en: str | None
    img_fr: str | None
    img_size_de: int | None
    img_size_en: int | None
    img_size_fr: int | None
    start_at_date: datetime | None = Field(sa_column=Column(Date(), nullable=True))
    start_at_time: datetime | None = Field(sa_column=Column(Time(timezone=False), nullable=True))
    end_at_date: datetime | None = Field(sa_column=Column(Date(), nullable=True))
    end_at_time: datetime | None = Field(sa_column=Column(Time(timezone=False), nullable=True))
    elements: int

    @staticmethod
    def get_zms_metaid():
        return 'UniBEEvent'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'teaser_de':        'eventTeaser_ger',
            'teaser_en':        'eventTeaser_eng',
            'teaser_fr':        'eventTeaser_fra',
            'img_de':           'eventBild_ger',
            'img_en':           'eventBild_eng',
            'img_fr':           'eventBild_fra',
            'img_size_de':      'eventBild_ger',
            'img_size_en':      'eventBild_eng',
            'img_size_fr':      'eventBild_fra',
            'start_at_date':    'eventStart',
            'start_at_time':    'eventStarttime',
            'end_at_date':      'eventEnd',
            'end_at_time':      'eventEndtime',
            'elements':         'obj.getObjChildren(e)',
        }


class WeiterbildungStudiengang(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    category: str | None
    subject_de: str | None
    subject_en: str | None
    subject_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None
    img: str | None
    img_size: int | None
    titleimg_de: str | None
    titleimg_en: str | None
    titleimg_fr: str | None
    titleimg_size_de: str | None
    titleimg_size_en: str | None
    titleimg_size_fr: str | None
    elements: int

    @staticmethod
    def get_zms_metaid():
        return 'weiterbildung_studiengang'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'category':         'rubrik',
            'subject_de':       'attr_dc_subject_ger',
            'subject_en':       'attr_dc_subject_eng',
            'subject_fr':       'attr_dc_subject_fra',
            'descr_de':         'attr_dc_description_ger',
            'descr_en':         'attr_dc_description_eng',
            'descr_fr':         'attr_dc_description_fra',
            'img':              'article_teaserbild',
            'img_size':         'article_teaserbild',
            'titleimg_de':      'titleimage_ger',
            'titleimg_en':      'titleimage_eng',
            'titleimg_fr':      'titleimage_fra',
            'titleimg_size_de': 'titleimage_ger',
            'titleimg_size_en': 'titleimage_eng',
            'titleimg_size_fr': 'titleimage_fra',
            'elements':         'obj.getObjChildren(e)',
        }


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
