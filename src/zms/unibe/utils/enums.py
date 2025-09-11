from enum import Enum


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
