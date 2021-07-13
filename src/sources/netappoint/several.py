from .netappoint_base import *


class Bonn(NetAppointBase):
    ID = "bonn"
    BASE_URL = "https://onlinetermine.bonn.de"
    NA_COMPANY = "stadtbonn"
    VERIFY_CERTIFICATE = False


class BonnBau(NetAppointBase):
    ID = "bonnbau"
    BASE_URL = "https://onlinetermine.bonn.de"
    NA_COMPANY = "stadtbonn-bau"
    VERIFY_CERTIFICATE = False


class Dresden(NetAppointBase):
    ID = "dresden"
    BASE_URL = "https://termine.dresden.de/netappoint"
    NA_COMPANY = "stadtdresden-fs"


class DresdenKfz(NetAppointBase):
    ID = "dresdenkfz"
    BASE_URL = "https://termine.dresden.de/netappoint"
    NA_COMPANY = "stadtdresden-kfz"


# TODO: Not working yet
#class Hamburg(NetAppointBase):
#    ID = "hamburg"
#    BASE_URL = "https://netappoint.de/hh/hamburg"
#    NA_COMPANY = "hamburg"


class KaiserslauternAusl(NetAppointBase):
    ID = "kaiserslauternausl"
    BASE_URL = "https://www3.kaiserslautern.de/netappoint"
    NA_COMPANY = "kaiserslautern-ausl"


class KreisBergstrasse(NetAppointBase):
    ID = "kreisbergstrasse"
    BASE_URL = "https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint"
    NA_COMPANY = "bergstrasse"


class KreisGermersheimKfz(NetAppointBase):
    ID = "kreisgermersheimkfz"
    BASE_URL = "https://kfz.kreis-germersheim.de/netappoint"
    NA_COMPANY = "kreis-germersheim"


class LeipzigStandesamt(NetAppointBase):
    ID = "leipzigstandesamt"
    BASE_URL = "https://adressen.leipzig.de/netappoint"
    NA_COMPANY = "leipzig-standesamt"
    NA_EXTRA_PARAMS = ["cur_causes=0|1|2"]


class Magdeburg(NetAppointBase):
    ID = "magdeburg"
    BASE_URL = "https://service.magdeburg.de/netappoint"
    NA_COMPANY = "magdeburg"
