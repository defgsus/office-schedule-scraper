from .etermin_base import *


HAND_PICKED = [
    ("asbtest", "Corona Testcenter", "ASBTestcenter"),
    ("bbmess", "Landesamt für Mess- und Eichwesen Berlin-Brandenburg", "lme-be-bb"),
    ("billerbeck", "Stadt Billerbeck Verwaltung", "termininbillerbeck"),
    ("blankenburg", "Stadt Blankenburg (Harz)", "blankenburg"),
    ("bonnjob", "Jobcenter Bonn", "jcbn"),
    ("braunschweigtest", "Corona Test Braunschweig", "coronatestbs"),
    ("burgendlandkaa", "Kammer für Arbeiter und Angestellte für das Burgenland", "GBRBgld"),
    ("butzbach", "Magistrat der Stadt Butzbach", "stadtbutzbach"),
    ("coesfeld", "Stadt Coesfeld", "coe"),
    ("lkcoesfeld", "Kreis Coesfeld", "kreiscoesfeld"),
    ("daunvg", "Verbandsgemeindeverwaltung Daun", "vgdaun"),
    ("dormagen", "Stadt Dormagen", "stadtdormagen"),
    ("deggendorf", "Landratsamt Deggendorf", "LRA-DEG-Termin"),
    ("duelmen", "Stadt Dülmen", "duelmen"),
    ("elitheratest", "Corona TESTZENTRUM im Elithera", "testzentrum1"),
    ("fuerthtest", "SARS-CoV-2 Testzentrum der Stadt Fürth", "Testzentrum_agnf"),
    ("geldernsw", "Stadtwerke Geldern Netz", "Zaehlerwechseltermine"),
    ("goslartest", "Testzentrum Goslar", "testzentrumgoslar"),
    ("graz", "Stadt Graz", "stadtgraz"),
    ("grazuni", "Universität Graz", "unitestet"),
    ("grazamt", "BürgerInnenamt Stadt Graz", "buergerinnenamt"),
    ("hahnenkleetest", "Testzentrum Hahnenklee", "testzentrumhahnenklee"),
    ("halbersadt", "Stadt Halberstadt", "halberstadt"),
    ("hammersbachtest", "Schnelltestzentrum Hammersbach", "Schnelltestzentrum"),
    ("hersfeldtest", "Corona-Testcenter Hersfeld-Rotenburg", "testcenter-hef-rof"),
    ("hsktest", "Hochsauerlandkreis", "hsk-schnelltest"),
    ("innsbruckpsych", "Psychologische Studierendenberatung Innsbruck", "PSB-Innsbruck"),
    ("itzehoe", "Stadt Itzehoe Einwohnermeldeamt", "Stadt_Itzehoe"),
    ("kreissteinfurt", "Kreis Steinfurt", "kreis-steinfurt"),
    ("lehrte", "Stadt Lehrte", "StadtLehrte"),
    ("mittenwalde", "Stadt Mittenwalde", "StadtMittenwalde"),
    ("olfen", "Stadt Olfen", "stadtolfen"),
    ("oberasbach", "Stadt Oberasbach", "stadtoberasbach"),
    ("oesterreichgk", "Österreichische Gesundheitskasse", "OEGK"),
    ("saluburggbr", "Gesundheitsberuferegister Arbeiterkammer Salzburg", "gbr"),
    ("selm", "Stadt Selm", "stadtselm"),
    ("stadtbergen", "Stadt Stadtbergen", "stadtbergen"),
    ("stahnsdorf", "Gemeinde Stahnsdorf", "stahnsdorf"),
    ("stuttgartpalais", "StadtPalais - Museum für Stuttgart", "stadtlaborstuttgart"),
    ("teublitztest", "Corona-Schnellteststelle Teublitz", "spitzwegapo"),
    ("walldorf", "Stadt Walldorf", "stadt-walldorf"),
    ("wedemarktest", "Corona-Schnelltestzentrum Caspar & Dase für die Wedemark", "Schnelltestungen"),
    ("weimarunioffice", "Bauhaus-Universität Weimar Erdgeschoss Raum 002", "international-office"),
    ("wiehl", "Stadt Wiehl", "stadtwiehl"),
]

"""
    TODO: find out where they belong to and complete
    ("ru1", "Abt. Bau- und Raumordnungsrecht", "ru1"),
    ("ru7", "Abt. Raumordnung und Gesamtverkehrsangelegenheiten", "ru7"),
    ("brueckenbau", "Abt. Brückenbau", "ST5"),  # http://www.noe.gv.at/noe/Kontakt-Landesverwaltung/Gruppe_Strasse.html
"""

for source_id, name, url_part in HAND_PICKED:
    exec(f"""
class AutoGen{source_id.capitalize()}(ETerminBase):
    ID = "{source_id}"
    ET_URL = "{url_part}"
    NAME = "{name}"
    """)