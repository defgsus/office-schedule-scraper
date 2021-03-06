"""
Going through https://www.kommunix.de/referenzen/

TODO: cities/institutions which are listed in reference page
    but which i did not find on the web.
    Erfurt: https://www.erfurt.de/ef/de/rathaus/bservice/index.html
    Hildburghausen
    Kyffhäuserkreis
    Mühlhausen
    Wartburgkreis/Bad Salzungen
    Gera
    Altenburg
    Eisenach
    Sonneberg
"""
from .tevis_base import *


class IlmKreisScraper(TevisBaseScraper):
    ID = "ilmkreis"
    NAME = "Ilm-Kreis"
    BASE_URL = "https://tvweb.ilm-kreis.de/ilmkreis"


class JenaScraper(TevisBaseScraper):
    ID = "jena"
    NAME = "Stadt Jena"
    BASE_URL = "https://tevis-bs.jena.de"


class NordhausenScraper(TevisBaseScraper):
    ID = "nordhausen"
    NAME = "Stadt Nordhausen"
    BASE_URL = "https://tevis.svndh.de"


class WeimarScraper(TevisBaseScraper):
    ID = "weimar"
    NAME = "Stadt Weimar"
    BASE_URL = "https://tevis.weimar.de"

