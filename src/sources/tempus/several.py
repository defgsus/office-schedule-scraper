from .tempus_base import TempusBaseScraper


HAND_PICKED = (
    # TODO: duesseldorfs have different options html
    #(1, 'duesseldorf', 'Stadt Düsseldorf'),
    #(6, 'duesseldorf2', 'Stadt Düsseldorf'),
    #(8, 'duesseldorfga', 'Stadt Düsseldorf Gesundheitsamt'),
    #(64, 'duesseldorfgb', 'Stadt Düsseldorf Gesundheitsberatung'),
    #(81, 'duesseldorf3', 'Stadt Düsseldorf'),
    (3, 'frankfurtba', 'Stadt Frankfurt am Main Bürgeramt'),
    (4, 'wuppertalsv', 'Stadt Wuppertal Staßenverkehrsamt'),
    # TODO: this one is pretty strange (webpage text says Berlin)
    #   and also does not have options
    #(7, 'wuppertal', 'Stadt Wuppertal'),
    (56, 'wuppertalewm', 'Stadt Wuppertal Einwohnermeldeamt'),
    (9, 'ludwigshafenaus', 'Stadt Ludwigshafen Ausländerbehörde'),
    (12, 'bielefeldkfz', 'Stadt Bielefeld Kfz-Zulassungsbehörde'),
    (54, 'bielefeldaus', 'Stadt Bielefeld Ausländerbehörde'),
    (58, 'bielefeldsa', 'Stadt Bielefeld Standesamt'),
    (83, 'bielefeldbb', 'Stadt Bielefeld Bürgerberatung'),
    (110, 'bielefeldfe', 'Stadt Bielefeld Fahrerlaubnisbehörde'),
    (13, 'ludwigsburg', 'Stadt Ludwigsburg'),
    (14, 'gelsenkirchen', 'Stadt Gelsenkirchen'),
    (15, 'luedenscheid', 'Stadt Lüdenscheid'),
    # TODO: They do not have option form elements
    #(17, 'uniduisburg', 'Universität Duisburg-Essen'),
    (23, 'bochumsw', 'Stadtwerke Bochum'),
    (127, 'bochum', 'Stadt Bochum'),
    (25, 'schriesheim', 'Stadt Schriesheim'),
    (27, 'werrameissner', 'Kreis Werra-Meißner'),
    (28, 'lauenburgkfz', 'Kreis Lauenburg Fachdienst Straßenverkehr'),
    (36, 'mannheimbs', 'Stadt Mannheim Bürgerservice'),
    (47, 'mannheimsa', 'Stadt Mannheim Fachbereich Sicherheit und Ordnung'),
    (38, 'herborn', 'Stadt Herborn'),
    (39, 'teltow', 'Stadt Teltow'),
    (41, 'eschwege', 'Stadt Eschwege'),
    (43, 'leichlingen', 'Stadt Leichlingen'),
    (45, 'kherfordkfz', 'Kreis Herford Straßenverkehrsamt'),
    # This is deactivated and replaced by self-hosted https://www.essen.de/rathaus/onlinetermine_der_stadtessen.de.html
    #   which is handled in essen.py
    #(48, 'essen', 'Stadt Essen'),
    (49, 'rheingautaunus', 'Rheingau-Taunus-Kreis'),
    (50, 'neuulm', 'Stadt Neu-Ulm'),
    (51, 'ostfildern', 'Ostfildern'),
    (57, 'luenen', 'Stadt Lünen'),
    (60, 'mannheimmvv', 'Stadtwerke Mannheim'),
    # TODO: They are very! different
    #(63, 'dortmundjob', 'Jobcenter Dortmund'),
    (66, 'giessen', 'Stadt Gießen'),
    (67, 'oberbergisch', 'Straßenverkehrsamt Oberbergischer Kreis'),
    (68, 'kronachkfz', 'Landkreis Kronach Zulassungsbehörde'),
    (69, 'ebersfeldwsw', 'Stadtwerke Ebersfeld'),
    (70, 'kielsw', 'Stadtwerke Kiel'),
    (71, 'burscheid', 'Stadt Burscheid'),
    (72, 'ravensburg', 'Stadt Ravensburg'),
    (76, 'weinheim', 'Stadt Weinheim'),
    (82, 'freising', 'Stadt Freising'),
    (84, 'ladenburg', 'Stadt Ladenburg'),
    (158, 'schwaebischhall', 'Stadt Schwäbisch Hall'),
    (86, 'schwaebischhallkfz', 'Landkreis Schwäbisch Hall Zulassungsstelle'),
    (87, 'rhedawiedenbrueck', 'Stadt Rheda-Wiedenbrück'),
    (88, 'lippstadtew', 'Stadt Lippstadt Fachdienst Einwohnerwesen'),
    (91, 'ansbach', 'Stadt Ansbach'),
    (92, 'krunnakfz', 'Kreis Unna Kfz'),
    # TODO: Their options form has no elements
    #(138, 'krunnaimpf', 'Kreis Unna Impfzentrum'),
    (95, 'badwaldsee', 'Stadt Bad Waldsee'),
    (99, 'beckum', 'Stadt Beckum'),
    (100, 'rottenburg', 'Stadt Rottenburg'),
    (101, 'bergischgladbach', 'Stadt Bergisch Gladbach'),
    (102, 'holtestukenbrock', 'Stadt Schloß Holte-Stukenbrock'),
    (103, 'freiberg', 'Stadt Freiberg'),
    (104, 'beckumschwimm', 'Stadt Beckum Schwimmbäder'),
    (105, 'kreisolpe', 'Kreis Olpe'),
    (106, 'overath', 'Stadt Overath'),
    (107, 'tuebingen', 'Stadt Tübingen'),
    (108, 'kuerten', 'Stadt Kürten'),
    (109, 'werne', 'Stadt Werne'),
    (111, 'oberding', 'Stadt Oberding'),
    (114, 'roesrath', 'Stadt Rösrath'),
    (115, 'ilvesheim', 'Gemeinde Ilvesheim'),
    (117, 'evo', 'EVO ServicePunkt'),
    (118, 'leimen', 'Stadt Leimen'),
    (122, 'nusloch', 'Gemeinde Nußloch'),
    (128, 'oldenburg', 'Landkreis Oldenburg'),
    (134, 'boenen', 'Gemeinde Bönen'),
    (136, 'herfordimpf', 'Kreis Herford Impfzentrum'),
    # TODO: their html might be quite different
    #(153, 'boeblingen', 'Kreis Böblingen'),
    (155, 'schwieberdingen', 'Stadt Schwieberdingen'),
    (161, 'bergkamen', 'Stadt Bergkamen'),
)


for tempus_id, source_id, name in HAND_PICKED:
    exec(f"""
class Tempus{tempus_id}(TempusBaseScraper):
    ID = "{source_id}"
    NAME = "{name}"
    TEMPUS_ID = {tempus_id}
    """)
