from .netappoint_base import *


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


class Magdeburg(NetAppointBase):
    ID = "magdeburg"
    NAME = "Stadt Magdeburg"
    BASE_URL = "https://service.magdeburg.de/netappoint"
    NA_COMPANY = "magdeburg"
