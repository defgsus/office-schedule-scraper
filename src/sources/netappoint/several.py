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