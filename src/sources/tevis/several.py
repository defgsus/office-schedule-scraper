from .tevis_base import *


class Amberg(TevisBaseScraper):
    ID = "amberg"
    BASE_URL = "https://termine.amberg.de/"


class Heidelberg(TevisBaseScraper):
    ID = "heidelberg"
    BASE_URL = "https://tevis-online.heidelberg.de"


class KreisWesel(TevisBaseScraper):
    ID = "kreiswesel"
    BASE_URL = "https://tevis.krzn.de/tevisweb080"


class Mainz(TevisBaseScraper):
    ID = "mainz"
    BASE_URL = "https://otv.mainz.de/"
