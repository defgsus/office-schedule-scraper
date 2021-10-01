from .tevis_base import *


class Amberg(TevisBaseScraper):
    ID = "amberg"
    NAME = "Stadt Amberg"
    BASE_URL = "https://termine.amberg.de"


class Friesland(TevisBaseScraper):
    ID = "friesland"
    NAME = "Landkreis Friesland"
    BASE_URL = "https://onlinetermine.friesland.de"


class Goeppingen(TevisBaseScraper):
    ID = "goeppingen"
    NAME = "Landkreis Goeppingen"
    BASE_URL = "https://termin.landkreis-goeppingen.de"


class Heidelberg(TevisBaseScraper):
    ID = "heidelberg"
    NAME = "Stadt Heidelberg"
    BASE_URL = "https://tevis-online.heidelberg.de"


# TODO: location name/title does not work for this page
class KielEma(TevisBaseScraper):
    ID = "kielema"
    NAME = "Kiel Einwohnermeldeamt"
    BASE_URL = "https://terminvergabe-ema-zulassung.kiel.de/tevisema"


class KreisSoest(TevisBaseScraper):
    ID = "kreissoest"
    NAME = "Kreis Soest"
    BASE_URL = "https://termine-buergerdienste.kreis-soest.de"


class KreisWesel(TevisBaseScraper):
    ID = "kreiswesel"
    NAME = "Kreis Wesel"  # or Kreis Viersen?
    BASE_URL = "https://tevis.krzn.de/tevisweb080"


class Ludwigshafen(TevisBaseScraper):
    ID = "ludwigshafen"
    NAME = "Kreis Ludwigshfen"
    BASE_URL = "https://tevisweb.ludwigshafen.de"


class Mainz(TevisBaseScraper):
    ID = "mainz"
    NAME = "Stadt Mainz"
    BASE_URL = "https://otv.mainz.de"


class MaerkischerKreis(TevisBaseScraper):
    ID = "maerkischerkreis"
    NAME = "Märkischer Kreis"
    BASE_URL = "https://terminvergabe.maerkischer-kreis.de"


class Muenster(TevisBaseScraper):
    ID = "muenster"
    NAME = "Stadt Muenster"
    BASE_URL = "https://termine.stadt-muenster.de"


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


class Salzlandkreis(TevisBaseScraper):
    ID = "salzlandkreis"
    NAME = "Salzlandkreis"
    BASE_URL = "https://termine.salzlandkreis.de"
    VERIFY_CERTIFICATE = False


class Verden(TevisBaseScraper):
    ID = "verden"
    NAME = "Landkreis Verden"
    BASE_URL = "https://lkv.landkreis-verden.de/TEVISWEB"
