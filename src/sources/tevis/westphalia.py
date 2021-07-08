"""
Going through https://www.kommunix.de/referenzen/

TODO: cities/institutions which are listed in referene page
    but which i did not find
    
"""
from .tevis_base import *


class KreisWeselScraper(TevisBaseScraper):
    ID = "kreiswesel"
    BASE_URL = "https://tevis.krzn.de/tevisweb080"

