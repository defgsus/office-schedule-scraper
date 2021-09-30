"""
The websites have been collected through websearch

    terminvereinbarung site:termine-reservieren.de

They are collectively hosted on https://termine-reservieren.de by Kommunix GmbH

"""
from .tevis_base import *


class TermineReservierenBase(TevisBaseScraper):
    # avoid parallel downloads on single server
    MULTI_PROCESS_GROUP = "termine-reservieren"


class BadKreuznach(TermineReservierenBase):
    ID = "badkreuznach"
    NAME = "Stadt Bad-Kreuznach"
    BASE_URL = "https://termine-reservieren.de/termine/svkh"


class BernkastelWittlich(TermineReservierenBase):
    ID = "bernkastelwittlich"
    NAME = "Landkreis Bernkastel-Wittlich"
    BASE_URL = "https://termine-reservieren.de/termine/bernkastel-wittlich"


class CochemZell(TermineReservierenBase):
    ID = "cochemzell"
    NAME = "Landkreis Cochem-Zell"
    BASE_URL = "https://termine-reservieren.de/termine/cochem-zell"


class Eislingen(TermineReservierenBase):
    ID = "eislingen"
    NAME = "Stadt Eislingen"
    BASE_URL = "https://termine-reservieren.de/termine/eislingen"


class Frankenthal(TermineReservierenBase):
    ID = "frankenthal"
    NAME = "Stadt Frankenthal"
    BASE_URL = "https://termine-reservieren.de/termine/frankenthal"


class Fulda(TermineReservierenBase):
    ID = "fulda"
    NAME = "Stadt Fulda"
    BASE_URL = "https://termine-reservieren.de/termine/fulda/"


class Gottmadingen(TermineReservierenBase):
    ID = "gottmadingen"
    NAME = "Gemeinde Gottmadingen"
    BASE_URL = "https://termine-reservieren.de/termine/gottmadingen"


class Gronau(TermineReservierenBase):
    ID = "gronau"
    NAME = "Stadt Gronau"
    BASE_URL = "https://termine-reservieren.de/termine/gronau"


class Hof(TermineReservierenBase):
    ID = "hof"
    NAME = "Stadt Hof"
    BASE_URL = "https://termine-reservieren.de/termine/hof"


class Ingelheim(TermineReservierenBase):
    ID = "ingelheim"
    NAME = "Stadt Ingelheim"
    BASE_URL = "https://termine-reservieren.de/termine/ingelheim"


class KfzGrasbrunn(TermineReservierenBase):
    ID = "kfzgrasbrunn"
    NAME = "Kfz Zulassungstelle Grasbrunn"
    BASE_URL = "https://termine-reservieren.de/termine/lramuenchen/kfz-zulassungsstelle-grasbrunn"


class LraZwickau(TermineReservierenBase):
    ID = "lkzwickau"
    NAME = "Landkreis Zwickau"
    BASE_URL = "https://termine-reservieren.de/termine/lra-zwickau"


class MayenKoblenz(TermineReservierenBase):
    ID = "kvmayenkoblenz"
    NAME = "Landkreis Mayen-Koblenz"
    BASE_URL = "https://termine-reservieren.de/termine/kvmayen-koblenz"


class Loehne(TermineReservierenBase):
    ID = "loehne"
    NAME = "Stadt Löhne"
    BASE_URL = "https://termine-reservieren.de/termine/loehne"


class Miesbach(TermineReservierenBase):
    ID = "lramiesbach"
    NAME = "Landratsamt Miesbach"
    BASE_URL = "https://termine-reservieren.de/termine/lra-miesbach"


class MuenchenAusl(TermineReservierenBase):
    ID = "lramuenchenausl"
    NAME = "Landkreis München Ausländerbehörde"
    BASE_URL = "https://termine-reservieren.de/termine/lramuenchen/auslaenderbehoerde"


class MuenchenEfa(TermineReservierenBase):
    ID = "lramuenchenefa"
    NAME = "Landratsamt München"
    BASE_URL = "https://termine-reservieren.de/termine/lramuenchen/efa"


class MuenchenJob(TermineReservierenBase):
    ID = "lramuenchenjob"
    NAME = "Landkreis München Jobcenter"
    BASE_URL = "https://amtonline.de/tvweb/jc-muenchen"


class Minden(TermineReservierenBase):
    ID = "minden"
    NAME = "Stadt Minden"
    BASE_URL = "https://termine-reservieren.de/termine/minden"


class Paderborn(TermineReservierenBase):
    ID = "paderborn"
    NAME = "Stadt Paderborn"
    BASE_URL = "https://termine-reservieren.de/termine/paderborn"


class Salzgitter(TermineReservierenBase):
    ID = "salzgitter"
    NAME = "Stadt Salzgitter"
    BASE_URL = "https://termine-reservieren.de/termine/salzgitter"


class SchoenebeckElbe(TermineReservierenBase):
    ID = "schoenebeckelbe"
    NAME = "Stadt Schönebeck (Elbe)"
    BASE_URL = "https://termine-reservieren.de/termine/schoenebeck-elbe"


class Speyer(TermineReservierenBase):
    ID = "speyer"
    NAME = "Stadt Speyer"
    BASE_URL = "https://termine-reservieren.de/termine/speyer"


class Stadtsoest(TermineReservierenBase):
    ID = "stadtsoest"
    NAME = "Stadt Söst"
    BASE_URL = "https://termine-reservieren.de/termine/stadtsoest"


class Steinburg(TermineReservierenBase):
    ID = "steinburg"
    NAME = "Stadt Steinburg"
    BASE_URL = "https://termine-reservieren.de/termine/steinburg"


class Trier(TermineReservierenBase):
    ID = "trier"
    NAME = "Stadt Trier"
    BASE_URL = "https://termine-reservieren.de/termine/trier"


class Unna(TermineReservierenBase):
    ID = "unna"
    NAME = "Stadt Unna"
    BASE_URL = "https://termine-reservieren.de/termine/unna"


class Weilheimschongau(TermineReservierenBase):
    ID = "weilheimschongau"
    NAME = "Landkreis Weilheim-Schongau"
    BASE_URL = "https://termine-reservieren.de/termine/weilheimschongau"


# TODO: they use a 'suggest' page which currently is not supported
#   e.g. https://termine-reservieren.de/termine/westerwaldkreis/suggest?mdt=540&select_cnc=1&cnc-1226=1&cnc-1229=0&cnc-1250=0&cnc-1235=0&cnc-1234=0&cnc-1230=0&cnc-1231=0&cnc-1232=0&cnc-1233=0&cnc-1237=0&cnc-1238=0&cnc-1239=0&cnc-1227=0&cnc-1228=0&cnc-1236=0&cnc-1241=0&cnc-1242=0&cnc-1243=0&cnc-1240=0&cnc-1244=0&cnc-1245=0&cnc-1246=0&cnc-1247=0&cnc-1248=0&cnc-1249=0
#class Westerwaldkreis(TermineReservierenBase):
#    ID = "westerwaldkreis"
#    NAME = "Kreis Westerwald"
#    BASE_URL = "https://termine-reservieren.de/termine/westerwaldkreis"


class Wittmund(TermineReservierenBase):
    ID = "wittmund"
    NAME = "Stadt Wittmund"
    BASE_URL = "https://termine-reservieren.de/termine/wittmund/stva"


class Worms(TermineReservierenBase):
    ID = "worms"
    NAME = "Stadt Worms"
    BASE_URL = "https://termine-reservieren.de/termine/worms"

