"""
All found below https://tevis.ekom21.de.

Using a searchengine with "Terminevergabe site:ekom21.de"
"""
from .tevis_base import *


class EgelsbachScraper(TevisBaseScraper):
    ID = "egelsbach"
    BASE_URL = "https://tevis.ekom21.de/egb"


class FrankfurtScraper(TevisBaseScraper):
    ID = "frankfurt"
    BASE_URL = "https://tevis.ekom21.de/fra"


class FriedrichsdorfScraper(TevisBaseScraper):
    ID = "friedrichsdorf"
    BASE_URL = "https://tevis.ekom21.de/frf"


class GrossUmstadtScraper(TevisBaseScraper):
    ID = "grossumstadt"
    BASE_URL = "https://tevis.ekom21.de/gad"


class HornbergScraper(TevisBaseScraper):
    ID = "hornberg"
    BASE_URL = "https://tevis.ekom21.de/hbe"


class HuenstettenScraper(TevisBaseScraper):
    ID = "huenstetten"
    BASE_URL = "https://tevis.ekom21.de/hsz"


class HuettenbergScraper(TevisBaseScraper):
    ID = "huettenberg"
    BASE_URL = "https://tevis.ekom21.de/htb"


class KasselScraper(TevisBaseScraper):
    ID = "kassel"
    BASE_URL = "https://tevis.ekom21.de/kas"


class KelsterbachScraper(TevisBaseScraper):
    ID = "kelsterbach"
    BASE_URL = "https://tevis.ekom21.de/keb"


class KreisGrossGerauScraper(TevisBaseScraper):
    ID = "kreisgrossgerau"
    BASE_URL = "https://tevis.ekom21.de/grg"


class LeunScraper(TevisBaseScraper):
    ID = "leun"
    BASE_URL = "https://tevis.ekom21.de/lnx"


class LinsengerichtScraper(TevisBaseScraper):
    ID = "linsengericht"
    BASE_URL = "https://tevis.ekom21.de/lsg"


class MoerlenbachScraper(TevisBaseScraper):
    ID = "moerlenbach"
    BASE_URL = "https://tevis.ekom21.de/mah"


class NeuIsenburgScraper(TevisBaseScraper):
    ID = "neuisenburg"
    BASE_URL = "https://tevis.ekom21.de/nis"


class NiedensteinScraper(TevisBaseScraper):
    ID = "niedenstein"
    BASE_URL = "https://tevis.ekom21.de/nsn"


class OberRamstadtScraper(TevisBaseScraper):
    ID = "oberramstadt"
    BASE_URL = "https://tevis.ekom21.de/oby"


class OffenbachScraper(TevisBaseScraper):
    ID = "offenbach"
    BASE_URL = "https://tevis.ekom21.de/off"


class PfungstadtScraper(TevisBaseScraper):
    ID = "pfungstadt"
    BASE_URL = "https://tevis.ekom21.de/pft"


class ViernheimScraper(TevisBaseScraper):
    ID = "viernheim"
    BASE_URL = "https://tevis.ekom21.de/vhx"


class WeiterstadtScraper(TevisBaseScraper):
    ID = "weiterstadt"
    BASE_URL = "https://tevis.ekom21.de/wdt"
