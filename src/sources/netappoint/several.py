from .netappoint_base import *


class BochumBau(NetAppointBase):
    ID = "bochumbau"
    NAME = "Stadt Bochum Baubürgeramt"
    BASE_URL = "https://terminvergabe.bochum.de"
    NA_COMPANY = "bochumbaub"
    NA_EXTRA_PARAMS = ("cur_cause=0", )


class BochumKfz(NetAppointBase):
    ID = "bochumkfz"
    NAME = "Stadt Bochum Büro für Kfz-Angelegenheiten"
    BASE_URL = "https://terminvergabe.bochum.de"
    NA_COMPANY = "bochumbb"
    NA_EXTRA_PARAMS = ("cur_cause=10", )


class BochumZulassung(NetAppointBase):
    ID = "bochumzl"
    NAME = "Stadt Bochum Zulassungsstelle"
    BASE_URL = "https://terminvergabe.bochum.de"
    NA_COMPANY = "bochum-stva"
    NA_EXTRA_PARAMS = ("cur_cause=0", )


class BochumZulassung2(NetAppointBase):
    ID = "bochumzl2"
    NAME = "Stadt Bochum Zulassungsstelle Umtausch"
    BASE_URL = "https://terminvergabe.bochum.de"
    NA_COMPANY = "bochum-stva"
    NA_EXTRA_PARAMS = ("cur_cause=1", )


class Bonn(NetAppointBase):
    ID = "bonn"
    NAME = "Stadt Bonn"
    BASE_URL = "https://onlinetermine.bonn.de"
    NA_COMPANY = "stadtbonn"
    VERIFY_CERTIFICATE = False


class BonnBau(NetAppointBase):
    ID = "bonnbau"
    NAME = "Stadt Bonn Bauamt"
    BASE_URL = "https://onlinetermine.bonn.de"
    NA_COMPANY = "stadtbonn-bau"
    VERIFY_CERTIFICATE = False


class Braunschweig(NetAppointBase):
    ID = "braunschweig"
    NAME = "Stadt Braunschweig"
    BASE_URL = "https://otr.braunschweig.de/netappoint"
    NA_COMPANY = "stadtbraunschweig"


class Dresden(NetAppointBase):
    ID = "dresden"
    NAME = "Stadt Dresden"
    BASE_URL = "https://termine.dresden.de/netappoint"
    NA_COMPANY = "stadtdresden-fs"


class DresdenKfz(NetAppointBase):
    ID = "dresdenkfz"
    NAME = "Stadt Dresden Kfz-Zulassungsbehörde"
    BASE_URL = "https://termine.dresden.de/netappoint"
    NA_COMPANY = "stadtdresden-kfz"


class Halle(NetAppointBase):
    ID = "halle"
    NAME = "Stadt Halle"
    BASE_URL = "https://ncu.halle.de"
    NA_COMPANY = "stadthalle"


# no appointments during pandemic...
#class Hamburg(NetAppointBase):
#    ID = "hamburg"
#    NAME = "Stadt Hamburg"
#    BASE_URL = "https://netappoint.de/hh/hamburg"
#    NA_COMPANY = "hamburg"


# TODO: "Standortwahl" is not implemented right
class Koeln(NetAppointBase):
    ID = "koeln"
    NAME = "Stadt Koeln"
    BASE_URL = "https://termine-online.stadt-koeln.de"
    NA_COMPANY = "stadtkoeln"


class KaiserslauternAusl(NetAppointBase):
    ID = "kaiserslauternausl"
    NAME = "Stadt Kaiserslautern Ausländerbehörde"
    BASE_URL = "https://www3.kaiserslautern.de/netappoint"
    NA_COMPANY = "kaiserslautern-ausl"


class KreisBergstrasse(NetAppointBase):
    ID = "kreisbergstrasse"
    NAME = "Kreis Bergstraße"
    BASE_URL = "https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint"
    NA_COMPANY = "bergstrasse"


class KreisGermersheimKfz(NetAppointBase):
    ID = "kreisgermersheimkfz"
    NAME = "Kreis Germersheim Kfz-Zulassungsbehörde"
    BASE_URL = "https://kfz.kreis-germersheim.de/netappoint"
    NA_COMPANY = "kreis-germersheim"


class LeipzigStandesamt(NetAppointBase):
    ID = "leipzigstandesamt"
    NAME = "Stadt Leipzig Standesamt"
    BASE_URL = "https://adressen.leipzig.de/netappoint"
    NA_COMPANY = "leipzig-standesamt"
    NA_EXTRA_PARAMS = ["cur_causes=0|1|2"]


class Leverkusen(NetAppointBase):
    ID = "leverkusen"
    NAME = "Zulassungsstelle Leverkusen"
    BASE_URL = "https://termine.leverkusen.de"
    NA_COMPANY = "LEV-Zulassung"
    NA_EXTRA_PARAMS = ["cur_cause=0"]


class LkBhKfz(NetAppointBase):
    ID = "lkbhkfz"
    NAME = "Landkreis Breisgau-Hochschwarzwald Kfz-Zulassungsbehörde"
    BASE_URL = "https://termin.lkbh.net"
    NA_COMPANY = "lkbh-zulassung"


class LkBhLw(NetAppointBase):
    ID = "lkbhlw"
    NAME = "Landkreis Breisgau-Hochschwarzwald Landwitschaft"
    BASE_URL = "https://termin.lkbh.net"
    NA_COMPANY = "lkbh-lw"


class Magdeburg(NetAppointBase):
    ID = "magdeburg"
    NAME = "Stadt Magdeburg"
    BASE_URL = "https://service.magdeburg.de/netappoint"
    NA_COMPANY = "magdeburg"


class SrAachen(NetAppointBase):
    ID = "sraachen"
    NAME = "Städteregion Aachen"
    BASE_URL = "https://terminmanagement.regioit-aachen.de/sr_aachen"
    NA_COMPANY = "staedteregion-aachen"


class WuppertalGeo(NetAppointBase):
    ID = "wuppertalgeo"
    NAME = "Stadt Wuppertal Geodatenzentrum"
    BASE_URL = "https://terminvergabe2.wuppertal.de"
    NA_COMPANY = "stadtwuppertal-geo"
    NA_EXTRA_PARAMS = ("cur_cause=0", )


class WuppertalGewerbe(NetAppointBase):
    ID = "wuppertalgw"
    NAME = "Stadt Wuppertal Gewerbecenter"
    BASE_URL = "https://terminvergabe2.wuppertal.de"
    NA_COMPANY = "wuppertal-gewerbe"
