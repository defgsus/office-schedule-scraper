from .netappoint_base import *


class Bonn(NetAppointBase):
    ID = "bonn"
    BASE_URL = "https://onlinetermine.bonn.de"
    NA_COMPANY = "stadtbonn"
    VERIFY_CERTIFICATE = False


class Dresden(NetAppointBase):
    ID = "dresden"
    BASE_URL = "https://termine.dresden.de/netappoint"
    NA_COMPANY = "stadtdresden-fs"


class KreisBergstrasse(NetAppointBase):
    ID = "kreisbergstrasse"
    BASE_URL = "https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint"
    NA_COMPANY = "bergstrasse"