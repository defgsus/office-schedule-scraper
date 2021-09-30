from .tevis_base import *


class Amberg(TevisBaseScraper):
    ID = "amberg"
    NAME = "Stadt Amberg"
    BASE_URL = "https://termine.amberg.de"


class Goeppingen(TevisBaseScraper):
    ID = "goeppingen"
    NAME = "Landkreis Goeppingen"
    BASE_URL = "https://termin.landkreis-goeppingen.de"


class Heidelberg(TevisBaseScraper):
    ID = "heidelberg"
    NAME = "Stadt Heidelberg"
    BASE_URL = "https://tevis-online.heidelberg.de"


class KreisSoest(TevisBaseScraper):
    ID = "kreissoest"
    NAME = "Kreis Soest"
    BASE_URL = "https://termine-buergerdienste.kreis-soest.de"


class KreisWesel(TevisBaseScraper):
    ID = "kreiswesel"
    NAME = "Kreis Wesel"
    BASE_URL = "https://tevis.krzn.de/tevisweb080"


class Mainz(TevisBaseScraper):
    ID = "mainz"
    NAME = "Stadt Mainz"
    BASE_URL = "https://otv.mainz.de"


class MaerkischerKreis(TevisBaseScraper):
    ID = "maerkischerkreis"
    NAME = "Märkischer Kreis"
    BASE_URL = "https://terminvergabe.maerkischer-kreis.de"


class LkOrtenau(TevisBaseScraper):
    ID = "lkortenau"
    NAME = "Landkreis Ortenau"
    BASE_URL = "https://www.termine.lraog.de"


class LraDachau(TevisBaseScraper):
    ID = "dachau"
    NAME = "Landratsamt Dachau"
    BASE_URL = "https://termine.landratsamt-dachau.de/tevis"


class Saarbruecken(TevisBaseScraper):
    ID = "saarbruecken"
    NAME = "Stadt Saarbrücken"
    BASE_URL = "https://terminvergabe.saarbruecken.de"

