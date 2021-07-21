from .tevis_base import *


class Amberg(TevisBaseScraper):
    ID = "amberg"
    NAME = "Stadt Amberg"
    BASE_URL = "https://termine.amberg.de/"


class Heidelberg(TevisBaseScraper):
    ID = "heidelberg"
    NAME = "Stadt Heidelberg"
    BASE_URL = "https://tevis-online.heidelberg.de"


class KreisWesel(TevisBaseScraper):
    ID = "kreiswesel"
    NAME = "Kreis Wesel"
    BASE_URL = "https://tevis.krzn.de/tevisweb080"


class Mainz(TevisBaseScraper):
    ID = "mainz"
    NAME = "Stadt Mainz"
    BASE_URL = "https://otv.mainz.de/"