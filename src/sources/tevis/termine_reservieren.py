"""
The websites have been collected through websearch

    terminvereinbarung site:termine-reservieren.de

They are collectively hosted on https://termine-reservieren.de by Kommunix GmbH

"""
from .tevis_base import *


class BadKreuznach(TevisBaseScraper):
    ID = "badkreuznach"
    BASE_URL = "https://termine-reservieren.de/termine/svkh/"


class BernkastelWittlich(TevisBaseScraper):
    ID = "bernkastelwittlich"
    BASE_URL = "https://termine-reservieren.de/termine/bernkastel-wittlich"


class CochemZell(TevisBaseScraper):
    ID = "cochemzell"
    BASE_URL = "https://termine-reservieren.de/termine/cochem-zell"


class Eislingen(TevisBaseScraper):
    ID = "eislingen"
    BASE_URL = "https://termine-reservieren.de/termine/eislingen"


class Frankenthal(TevisBaseScraper):
    ID = "frankenthal"
    BASE_URL = "https://termine-reservieren.de/termine/frankenthal"


class Gronau(TevisBaseScraper):
    ID = "gronau"
    BASE_URL = "https://termine-reservieren.de/termine/gronau"


class Hof(TevisBaseScraper):
    ID = "hof"
    BASE_URL = "https://termine-reservieren.de/termine/hof"


class Ingelheim(TevisBaseScraper):
    ID = "ingelheim"
    BASE_URL = "https://termine-reservieren.de/termine/ingelheim"


class MayenKoblenz(TevisBaseScraper):
    ID = "kvmayenkoblenz"
    BASE_URL = "https://termine-reservieren.de/termine/kvmayen-koblenz"


class Loehne(TevisBaseScraper):
    ID = "loehne"
    BASE_URL = "https://termine-reservieren.de/termine/loehne"


class Miesbach(TevisBaseScraper):
    ID = "lramiesbach"
    BASE_URL = "https://termine-reservieren.de/termine/lra-miesbach"


class Muenchenefa(TevisBaseScraper):
    ID = "lramuenchenefa"
    BASE_URL = "https://termine-reservieren.de/termine/lramuenchen/efa"


class Minden(TevisBaseScraper):
    ID = "minden"
    BASE_URL = "https://termine-reservieren.de/termine/minden"


class Paderborn(TevisBaseScraper):
    ID = "paderborn"
    BASE_URL = "https://termine-reservieren.de/termine/paderborn"


class Salzgitter(TevisBaseScraper):
    ID = "salzgitter"
    BASE_URL = "https://termine-reservieren.de/termine/salzgitter"


class SchoenebeckElbe(TevisBaseScraper):
    ID = "schoenebeckelbe"
    BASE_URL = "https://termine-reservieren.de/termine/schoenebeck-elbe"


class Speyer(TevisBaseScraper):
    ID = "speyer"
    BASE_URL = "https://termine-reservieren.de/termine/speyer"


class Stadtsoest(TevisBaseScraper):
    ID = "stadtsoest"
    BASE_URL = "https://termine-reservieren.de/termine/stadtsoest"


class Steinburg(TevisBaseScraper):
    ID = "steinburg"
    BASE_URL = "https://termine-reservieren.de/termine/steinburg"


class Trier(TevisBaseScraper):
    ID = "trier"
    BASE_URL = "https://termine-reservieren.de/termine/trier"


class Unna(TevisBaseScraper):
    ID = "unna"
    BASE_URL = "https://termine-reservieren.de/termine/unna"


class Weilheimschongau(TevisBaseScraper):
    ID = "weilheimschongau"
    BASE_URL = "https://termine-reservieren.de/termine/weilheimschongau"


# TODO: they use a 'suggest' page which currently is not supported
#   e.g. https://termine-reservieren.de/termine/westerwaldkreis/suggest?mdt=540&select_cnc=1&cnc-1226=1&cnc-1229=0&cnc-1250=0&cnc-1235=0&cnc-1234=0&cnc-1230=0&cnc-1231=0&cnc-1232=0&cnc-1233=0&cnc-1237=0&cnc-1238=0&cnc-1239=0&cnc-1227=0&cnc-1228=0&cnc-1236=0&cnc-1241=0&cnc-1242=0&cnc-1243=0&cnc-1240=0&cnc-1244=0&cnc-1245=0&cnc-1246=0&cnc-1247=0&cnc-1248=0&cnc-1249=0
#class Westerwaldkreis(TevisBaseScraper):
#    ID = "westerwaldkreis"
#    BASE_URL = "https://termine-reservieren.de/termine/westerwaldkreis"


class Wittmund(TevisBaseScraper):
    ID = "wittmund"
    BASE_URL = "https://termine-reservieren.de/termine/wittmund/stva"


class Worms(TevisBaseScraper):
    ID = "worms"
    BASE_URL = "https://termine-reservieren.de/termine/worms"

