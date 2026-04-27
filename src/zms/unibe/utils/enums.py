from enum import Enum


class Locale(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-1
    de = "de"
    en = "en"
    fr = "fr"


class Lang(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-3
    de = "ger"
    en = "eng"
    fr = "fra"


class SiteType(str, Enum):
    Fakultaet = "Fakultaet"
    Departement = "Departement"
    Institut = "Institut"
    Abteilung = "Abteilung"
    Bereich = "Bereich"
    Einrichtung = "Einrichtung"
    Microsite = "Microsite"
    Library = "Library"
    Unisport = "Unisport"
    

class ContentModel(str, Enum):
    UniaktuellArticle = "UniaktuellArticle"
    ZMSAgenda = "ZMSAgenda"
    ZMSBoris = "ZMSBoris"
    ZMSDataTable = "ZMSDataTable"
    ZMSFormulator = "ZMSFormulator"
    ZMS = "ZMS"
    ZMSDocument = "ZMSDocument"
    ZMSFigure = "ZMSFigure"
    ZMSFile = "ZMSFile"
    ZMSFlexbox = "ZMSFlexbox"
    ZMSFolder = "ZMSFolder"
    ZMSGraphic = "ZMSGraphic"
    ZMSLinkContainer = "ZMSLinkContainer"
    ZMSLinkElement = "ZMSLinkElement"
    ZMSNote = "ZMSNote"
    ZMSObjectSet = "ZMSObjectSet"
    ZMSRecordSet = "ZMSRecordSet"
    ZMSRichtext = "ZMSRichtext"
    ZMSSqlDb = "ZMSSqlDb"
    ZMSTable = "ZMSTable"
    ZMSTeaserContainer = "ZMSTeaserContainer"
    ZMSTeaserElement = "ZMSTeaserElement"
    ZMSTextarea = "ZMSTextarea"
    ZMSVideo = "ZMSVideo"


class ImageVariant(str, Enum):
    img = "img"
    imghires = "imghires"
    imgsuperres = "imgsuperres"


class LabelPrefix(str, Enum):
    UniaktuellArticle = "UA_"
    ZMSAgenda = "ZMSAgenda."
    ZMSFormulator = "zms.formulator.lib."
    ZMSTable = "ZMSTable."
