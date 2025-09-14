from enum import Enum

# TODO: align Locale/Lang handle according to zms-fastapi refactoring
#
# class Locale(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-1
#     de = "de"
#     en = "en"
#     fr = "fr"
# 
# 
# class Lang(str, Enum):  # https://en.wikipedia.org/wiki/ISO_639-3
#     de = "ger"
#     en = "eng"
#     fr = "fra"


class Lang(str, Enum):
    de = 'de'
    en = 'en'
    fr = 'fr'


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
