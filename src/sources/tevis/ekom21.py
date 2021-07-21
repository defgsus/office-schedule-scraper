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
    NAME = "Stadt Egelsbach"
    BASE_URL = "https://tevis.ekom21.de/egb"


class FrankfurtScraper(Ekom21Base):
    ID = "frankfurt"
    NAME = "Stadt Frankfurt"
    BASE_URL = "https://tevis.ekom21.de/fra"


class FriedrichsdorfScraper(Ekom21Base):
    ID = "friedrichsdorf"
    NAME = "Stadt Friedrichsdorf"
    BASE_URL = "https://tevis.ekom21.de/frf"


class GrossUmstadtScraper(Ekom21Base):
    ID = "grossumstadt"
    NAME = "Stadt Groß-Umstadt"
    BASE_URL = "https://tevis.ekom21.de/gad"


class HornbergScraper(Ekom21Base):
    ID = "hornberg"
    NAME = "Stadt Hornberg"
    BASE_URL = "https://tevis.ekom21.de/hbe"


class HuenstettenScraper(Ekom21Base):
    ID = "huenstetten"
    NAME = "Stadt Hünstetten"
    BASE_URL = "https://tevis.ekom21.de/hsz"


class HuettenbergScraper(Ekom21Base):
    ID = "huettenberg"
    NAME = "Stadt Hüttenberg"
    BASE_URL = "https://tevis.ekom21.de/htb"


class KasselScraper(Ekom21Base):
    ID = "kassel"
    NAME = "Stadt Kassel"
    BASE_URL = "https://tevis.ekom21.de/kas"


class KelsterbachScraper(Ekom21Base):
    ID = "kelsterbach"
    NAME = "Stadt Kelsterbach"
    BASE_URL = "https://tevis.ekom21.de/keb"


class KreisGrossGerauScraper(Ekom21Base):
    ID = "kreisgrossgerau"
    NAME = "Kreis Groß-Gerau"
    BASE_URL = "https://tevis.ekom21.de/grg"


class LeunScraper(Ekom21Base):
    ID = "leun"
    NAME = "Stadt Leun"
    BASE_URL = "https://tevis.ekom21.de/lnx"


class LinsengerichtScraper(Ekom21Base):
    ID = "linsengericht"
    NAME = "Stadt Linsengericht"
    BASE_URL = "https://tevis.ekom21.de/lsg"


class MoerlenbachScraper(Ekom21Base):
    ID = "moerlenbach"
    NAME = "Stadt Mörlenbach"
    BASE_URL = "https://tevis.ekom21.de/mah"


class NeuIsenburgScraper(Ekom21Base):
    ID = "neuisenburg"
    NAME = "Stadt Neu-Isenburg"
    BASE_URL = "https://tevis.ekom21.de/nis"


class NiedensteinScraper(Ekom21Base):
    ID = "niedenstein"
    NAME = "Stadt Niedenstein"
    BASE_URL = "https://tevis.ekom21.de/nsn"


class OberRamstadtScraper(Ekom21Base):
    ID = "oberramstadt"
    NAME = "Stadt Ober-Ramstadt"
    BASE_URL = "https://tevis.ekom21.de/oby"


class OffenbachScraper(Ekom21Base):
    ID = "offenbach"
    NAME = "Stadt Offenbach"
    BASE_URL = "https://tevis.ekom21.de/off"


class PfungstadtScraper(Ekom21Base):
    ID = "pfungstadt"
    NAME = "Stadt Pfungstadt"
    BASE_URL = "https://tevis.ekom21.de/pft"


class ViernheimScraper(Ekom21Base):
    ID = "viernheim"
    NAME = "Stadt Viernheim"
    BASE_URL = "https://tevis.ekom21.de/vhx"


class WeiterstadtScraper(Ekom21Base):
    ID = "weiterstadt"
    NAME = "Stadt Weiterstadt"
    BASE_URL = "https://tevis.ekom21.de/wdt"
