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
    Uniaktuell = "Uniaktuell"
    ZMSAgenda = "ZMSAgenda"
    ZMSBoris = "ZMSBoris"
    ZMSDataTable = "ZMSDataTable"
    ZMSFile = "ZMSFile"
    ZMSFormulator = "ZMSFormulator"
    ZMSGraphic = "ZMSGraphic"


class ImageVariant(str, Enum):
    img = "img"
    imghires = "imghires"
    imgsuperres = "imgsuperres"


class LabelPrefix(str, Enum):
    Uniaktuell = "UA_"
    ZMSAgenda = "ZMSAgenda."
    ZMSFormulator = "zms.formulator.lib."
