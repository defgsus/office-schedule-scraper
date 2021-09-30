from .tevis_base import *


class MvnetBase(TevisBaseScraper):
    MULTI_PROCESS_GROUP = "mvnet"


class Greifswald(MvnetBase):
    ID = "greifswald"
    NAME = "Stadt Greifswald"
    BASE_URL = "https://tevis-online.mvnet.de/greifswald"


class Kluetzerwinkel(MvnetBase):
    ID = "kluetzerwinkel"
    NAME = "Amt Kluetzer Winkel"
    BASE_URL = "https://tevis-online.mvnet.de/kluetzerwinkel"


class Wismar(MvnetBase):
    ID = "wismar"
    NAME = "Hansestadt Wismar"
    BASE_URL = "https://tevis-online.mvnet.de/wismar"
