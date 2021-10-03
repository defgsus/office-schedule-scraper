from .tempus_base import *



class TempusEssenBase(TempusBaseScraper):
    BASE_URL = "https://meintermin.essen.de/termine/index.php"


class TempusEssen(TempusEssenBase):
    ID = "kressen"
    NAME = "Kreis Essen Bürgeramt"
    TEMPUS_ID = 21
    TEMPUS_EXTRA_PARAMS = ("anwendung=332", )


class TempusEssenKfz(TempusEssenBase):
    ID = "kressenkfz"
    NAME = "Kreis Essen Kfz.-Zulassungsbehörde"
    TEMPUS_ID = 21
    TEMPUS_EXTRA_PARAMS = ("anwendung=3352", )


class TempusEssenFahr(TempusEssenBase):
    ID = "kressenfa"
    NAME = "Kreis Essen Fahrerlaubnisbehörde"
    TEMPUS_ID = 21
    TEMPUS_EXTRA_PARAMS = ("anwendung=3354", )


class TempusEssenBorbeckKfz(TempusEssenBase):
    ID = "essenborbeckkfz"
    NAME = "Kfz.-Zulassungs- u. Fahrerlaubnisbehörde Essen-Borbeck"
    TEMPUS_ID = 21
    TEMPUS_EXTRA_PARAMS = ("anwendung=3356", )


class TempusEssenSozialEltern(TempusEssenBase):
    ID = "kressensoze"
    NAME = "Kreis Essen Elterngeld"
    TEMPUS_ID = 89
    TEMPUS_EXTRA_PARAMS = ("anwendung=1", )


class TempusEssenSozialWohn(TempusEssenBase):
    ID = "kressensozw"
    NAME = "Kreis Essen Wohngeld"
    TEMPUS_ID = 89
    TEMPUS_EXTRA_PARAMS = ("anwendung=3", )
