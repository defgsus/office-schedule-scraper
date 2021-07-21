"""
All found below https://tevis.ekom21.de.

Using a searchengine with "Terminevergabe site:ekom21.de"
"""
from .tevis_base import *


class Ekom21Base(TevisBaseScraper):
    # avoid parallel downloads on single server
    MULTI_PROCESS_GROUP = "ekom21"


class EgelsbachScraper(Ekom21Base):
    ID = "egelsbach"
    BASE_URL = "https://tevis.ekom21.de/egb"


class FrankfurtScraper(Ekom21Base):
    ID = "frankfurt"
    BASE_URL = "https://tevis.ekom21.de/fra"


class FriedrichsdorfScraper(Ekom21Base):
    ID = "friedrichsdorf"
    BASE_URL = "https://tevis.ekom21.de/frf"


class GrossUmstadtScraper(Ekom21Base):
    ID = "grossumstadt"
    BASE_URL = "https://tevis.ekom21.de/gad"


class HornbergScraper(Ekom21Base):
    ID = "hornberg"
    BASE_URL = "https://tevis.ekom21.de/hbe"


class HuenstettenScraper(Ekom21Base):
    ID = "huenstetten"
    BASE_URL = "https://tevis.ekom21.de/hsz"


class HuettenbergScraper(Ekom21Base):
    ID = "huettenberg"
    BASE_URL = "https://tevis.ekom21.de/htb"


class KasselScraper(Ekom21Base):
    ID = "kassel"
    BASE_URL = "https://tevis.ekom21.de/kas"


class KelsterbachScraper(Ekom21Base):
    ID = "kelsterbach"
    BASE_URL = "https://tevis.ekom21.de/keb"


class KreisGrossGerauScraper(Ekom21Base):
    ID = "kreisgrossgerau"
    BASE_URL = "https://tevis.ekom21.de/grg"


class LeunScraper(Ekom21Base):
    ID = "leun"
    BASE_URL = "https://tevis.ekom21.de/lnx"


class LinsengerichtScraper(Ekom21Base):
    ID = "linsengericht"
    BASE_URL = "https://tevis.ekom21.de/lsg"


class MoerlenbachScraper(Ekom21Base):
    ID = "moerlenbach"
    BASE_URL = "https://tevis.ekom21.de/mah"


class NeuIsenburgScraper(Ekom21Base):
    ID = "neuisenburg"
    BASE_URL = "https://tevis.ekom21.de/nis"


class NiedensteinScraper(Ekom21Base):
    ID = "niedenstein"
    BASE_URL = "https://tevis.ekom21.de/nsn"


class OberRamstadtScraper(Ekom21Base):
    ID = "oberramstadt"
    BASE_URL = "https://tevis.ekom21.de/oby"


class OffenbachScraper(Ekom21Base):
    ID = "offenbach"
    BASE_URL = "https://tevis.ekom21.de/off"


class PfungstadtScraper(Ekom21Base):
    ID = "pfungstadt"
    BASE_URL = "https://tevis.ekom21.de/pft"


class ViernheimScraper(Ekom21Base):
    ID = "viernheim"
    BASE_URL = "https://tevis.ekom21.de/vhx"


class WeiterstadtScraper(Ekom21Base):
    ID = "weiterstadt"
    BASE_URL = "https://tevis.ekom21.de/wdt"
