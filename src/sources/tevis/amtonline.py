from .tevis_base import *


class AmtOnlineBase(TevisBaseScraper):
    MULTI_PROCESS_GROUP = "amtonline"


# They seem to not use the interface - no offices listed
#class Lueneburg(AmtOnlineBase):
#    ID = "lueneburg"
#    NAME = "Hansestadt Lüneburg"
#    BASE_URL = "https://amtonline.de/tvweb/lueneburg"


class Mechernich(AmtOnlineBase):
    ID = "mechernich"
    NAME = "Stadt Mechernich"
    BASE_URL = "https://amtonline.de/tvweb/mechernich"


class MuenchenJob(AmtOnlineBase):
    ID = "lramuenchenjob"
    NAME = "Landkreis München Jobcenter"
    BASE_URL = "https://amtonline.de/tvweb/jc-muenchen"


class Radolfzell(AmtOnlineBase):
    ID = "radolfzell"
    NAME = "Stadt Radolfzell"
    BASE_URL = "https://amtonline.de/tvweb/radolfzell"
