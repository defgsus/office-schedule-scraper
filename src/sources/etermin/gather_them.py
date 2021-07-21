"""
    websearch: 'Buchen Sie hier Ihren Termin bei der Stadt site:etermin.net'

    l=[]; for (const e of document.querySelectorAll(".result__body")) {
      l.push({title: e.querySelector(".result__title a").text, url: e.querySelector(".result__url").href});
    } console.log(JSON.stringify(l))

"""


RESULTS = [
    {
        "title": "Stadt Graz - Online Termin buchen",
        "url": "https://www.etermin.net/o/stadtgraz/serviceid/152600"
    },
    {
        "title": "Stadt Graz | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtgraz/serviceid/151401"
    },
    {
        "title": "Stadt Lehrte | Sie haben noch kein Konto?",
        "url": "https://www.etermin.net/StadtLehrte"
    },
    {
        "title": "Stadt Billerbeck Verwaltung | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/termininbillerbeck"
    },
    {
        "title": "Stadt Dormagen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtdormagen"
    },
    {
        "title": "C&L Elmshorn - Terminkalender - Hier Termin buchen!",
        "url": "https://www.etermin.net/fluedke"
    },
    {
        "title": "SARS-CoV-2 Testzentrum der Stadt F\u00fcrth und des Landkreises F\u00fcrth",
        "url": "https://www.etermin.net/Testzentrum_agnf"
    },
    {
        "title": "Magistrat der Stadt Butzbach | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtbutzbach"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen/serviceid/169294"
    },
    {
        "title": "Buchen Sie hier Ihren Termin bei Sch\u00f6ner Reisen",
        "url": "https://www.etermin.net/sebastianrosmus"
    },
    {
        "title": "Stadt Halberstadt | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/halberstadt?calendarid=83869"
    },
    {
        "title": "Stadt Stadtbergen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtbergen?servicegroupid=65243,65547,65549,65757"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen?servicegroupid=70129,70012,70127,70128,70144,70146,70142,70154,70157,70160,70161,70162"
    },
    {
        "title": "Stadt Wiehl | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtwiehl"
    },
    {
        "title": "Stadt Itzehoe Einwohnermeldeamt | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/Stadt_Itzehoe"
    },
    {
        "title": "Stadt Graz | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtgraz?servicegroupid=68513"
    },
    {
        "title": "Wie \u00e4ndere ich die Ansicht der Eintr\u00e4ge im Terminkalender?",
        "url": "https://support.etermin.net/hc/de/articles/360025495531-Wie-\u2026A4ndere-ich-die-Ansicht-der-Eintr%C3%A4ge-im-Terminkalender-"
    },
    {
        "title": "Buchen Sie jetzt Ihren Termin direkt online bei uns!",
        "url": "https://www.etermin.net/o/drcaspari"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen?servicegroupid=70129,70012,7\u20266,70142,70154,70157,70160,70161,70162&serviceidpresel=169269"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen?servicegroupid=72269"
    },
    {
        "title": "B\u00fcrgerInnenamt Stadt Graz | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/buergerinnenamt?servicegroupid=75630"
    },
    {
        "title": "eTermin Fahrschule DEMO - Online Termin buchen",
        "url": "https://www.etermin.net/fahrschule/1/terminvereinbarung-online"
    },
    {
        "title": "Buchen Sie jetzt Ihren Gratis Antigen-Schnelltest bei der...",
        "url": "https://www.etermin.net/riedborn-apotheke"
    },
    {
        "title": "auditbee - Wirtschaftspr\u00fcfer Ren\u00e9 Respondek | Termin Online buchen",
        "url": "https://www.etermin.net/auditbee"
    },
    {
        "title": "Buche hier deinen Amazing Brautmode M\u00fcnchen Termin",
        "url": "https://www.etermin.net/amazing-brautmoden"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen?servicegroupid=70129,70012,7\u20266,70142,70154,70157,70160,70161,70162&serviceidpresel=169046"
    },
    {
        "title": "Stadt D\u00fclmen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/duelmen?servicegroupid=70129,70012,7\u20266,70142,70154,70157,70160,70161,70162&serviceidpresel=170765"
    },
    {
        "title": "Stadt Halberstadt | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/halberstadt?calendarid=83883"
    },
    {
        "title": "Reiseagentur Vospohl ...der Termin f\u00fcr deinen Urlaub",
        "url": "https://www.etermin.net/vossy"
    },
    {
        "title": "Buchen Sie jetzt Ihren Termin direkt online bei uns!",
        "url": "https://www.etermin.net/drcaspari"
    },
    {
        "title": "PonyTruppe Dresden - Online Termin buchen",
        "url": "https://www.etermin.net/PonyTruppeDresden"
    },
    {
        "title": "Abt. Bau- und Raumordnungsrecht | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/ru1"
    },
    {
        "title": "\u00d6sterreichische Gesundheitskasse | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/oegk"
    },
    {
        "title": "Reitsimulator Schweiz - Reiten mit Technik. Sitzschulung f\u00fcr Anf\u00e4nger...",
        "url": "https://www.etermin.net/reitsimulator"
    },
    {
        "title": "Abt. Raumordnung und Gesamtverkehrsangelegenheiten",
        "url": "https://www.etermin.net/ru7"
    },
    {
        "title": "Stadt Mittenwalde - Online Termin buchen",
        "url": "https://www.etermin.net/StadtMittenwalde"
    },
    {
        "title": "abat AG - Online Termin buchen",
        "url": "https://www.etermin.net/abat"
    },
    {
        "title": "Kreisj\u00e4gervereinigung B\u00f6blingen e.V. Schie\u00dfstand",
        "url": "https://www.etermin.net/KJVBB"
    },
    {
        "title": "Restaurant DEMO Online Tischreservierung",
        "url": "https://www.etermin.net/restaurant1"
    },
    {
        "title": "ASSARTO Unternehmensgruppe Schneider GbR - Schmuck-Schmiede...",
        "url": "https://www.etermin.net/Schmuckschmiede"
    },
    {
        "title": "C&L Elmshorn - Terminkalender - Hier Termin buchen!",
        "url": "https://www.etermin.net/fluedke/calendarid/70421"
    },
    {
        "title": "Privater Rettungsdienst Stadler | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/TestzentrumDeggendorf"
    },
    {
        "title": "StadtPalais - Museum f\u00fcr Stuttgart - Online Termin buchen",
        "url": "https://www.etermin.net/stadtlaborstuttgart"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/leonberg_honal"
    },
    {
        "title": "Stadt Blankenburg (Harz) | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/blankenburg"
    },
    {
        "title": "Jetzt Termin online vereinbaren bei SCHUBERT STONE",
        "url": "https://www.etermin.net/schubertstone"
    },
    {
        "title": "Corona-Schnelltestzentrum Caspar & Dase f\u00fcr die Wedemark und...",
        "url": "https://www.etermin.net/Schnelltestungen"
    },
    {
        "title": "Cindia Rheinwalt - Online Termin buchen",
        "url": "https://www.etermin.net/cindia"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/functions"
    },
    {
        "title": "Johannes Cloesters IT-Support - Online Termin buchen",
        "url": "https://www.etermin.net/jcitsupport"
    },
    {
        "title": "Termin mit Reinhard Krechler | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/krechler/serviceid/149491"
    },
    {
        "title": "Schnelltestzentrum Hammersbach (B\u00fcrgertreff), Am Alten Friedhof...",
        "url": "https://www.etermin.net/Schnelltestzentrum"
    },
    {
        "title": "Wirtschaft unter Strom - Online Termin buchen",
        "url": "https://www.etermin.net/gewerbe-basel"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/probefahrtvn"
    },
    {
        "title": "Tobias Witzenberger | Ergotherapie und Coaching in Hannover",
        "url": "https://www.etermin.net/tobias-witzenberger"
    },
    {
        "title": "Wolfgang Tatzel - Online Termin buchen",
        "url": "https://www.etermin.net/zahnzeh"
    },
    {
        "title": "eTermin Buchungssystem Beratungstermin buchen",
        "url": "https://www.etermin.net/o/etermin"
    },
    {
        "title": "Landesamt f\u00fcr Mess- und Eichwesen Berlin-Brandenburg",
        "url": "https://www.etermin.net/lme-be-bb"
    },
    {
        "title": "Mainfr\u00e4nkische Werkst\u00e4tten GmbH - Online Termin buchen",
        "url": "https://www.etermin.net/tierpark-sommerhausen"
    },
    {
        "title": "Berliner Teamschmie.de | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/zytariuk"
    },
    {
        "title": "Hermann Scherer - Online Termin buchen",
        "url": "https://www.etermin.net/hermannscherer"
    },
    {
        "title": "Freies Gymnasium Borsdorf | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/FGB"
    },
    {
        "title": "Werkstatt Termin Buchung OPEL Hyundai Service Inspektion...",
        "url": "https://www.etermin.net/auto-team"
    },
    {
        "title": "MARIANNE FUST - Online Termin buchen",
        "url": "https://www.etermin.net/MarianneFust"
    },
    {
        "title": "Die W\u00e4scherei - Das M\u00f6belhaus | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/diewaescherei"
    },
    {
        "title": "W. Schnieder GmbH & Co. KG | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/schnieder"
    },
    {
        "title": "Permanent Make-up Termine in K\u00f6ln, Hamburg und der Eifel",
        "url": "https://www.etermin.net/miderma"
    },
    {
        "title": "Wirtschaft unter Strom - Online Termin buchen",
        "url": "https://www.etermin.net/o/gewerbe-basel"
    },
    {
        "title": "Georg Niebler Naturschlafberater | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/der-niebler"
    },
    {
        "title": "Autozentrum Ries - Online Termin buchen",
        "url": "https://www.etermin.net/autozentrum-ries"
    },
    {
        "title": "Pflege- und Betreuungsdienst Kremer GmbH in Kooperation mit der...",
        "url": "https://www.etermin.net/schnelltest_hasselroth"
    },
    {
        "title": "Austrian Touch Die Kraft der Alpen f\u00fcr mehr Ausdauer, Energie und...",
        "url": "https://www.etermin.net/AustrianTouch"
    },
    {
        "title": "B\u00e4ren-Apotheke OG | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/baeren-apo"
    },
    {
        "title": "Gratis 3D Zahn Scan buchen. Unsichtbare Smiletogo Zahnspangen...",
        "url": "https://www.etermin.net/foryoufirst/serviceid/79210?lang=de"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/dk"
    },
    {
        "title": "Praxis f\u00fcr Arbeits- & Pr\u00e4ventivmedizin",
        "url": "https://www.etermin.net/papmed"
    },
    {
        "title": "Termin buchen | Wie m\u00f6chten Sie bezahlen?",
        "url": "https://www.etermin.net/sladkowski"
    },
    {
        "title": "Reiseb\u00fcro REISE NACH .. | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/REISENACH"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/benderfranklth"
    },
    {
        "title": "L&S GmbH & Co. KG - Online Termin buchen",
        "url": "https://www.etermin.net/lunds"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/benderfranklth"
    },
    {
        "title": "L&S GmbH & Co. KG - Online Termin buchen",
        "url": "https://www.etermin.net/lunds"
    },
    {
        "title": "Stadtwerke Geldern Netz | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/Zaehlerwechseltermine"
    },
    {
        "title": "eTermin online buchen | MINI Hamburg",
        "url": "https://www.etermin.net/mini-hamburg"
    },
    {
        "title": "TR Tino Richter Schuldnerberatung M\u00fcnchen - Online Termin buchen",
        "url": "https://www.etermin.net/tr1"
    },
    {
        "title": "Bauhaus-Universit\u00e4t Weimar Erdgeschoss Raum 002/ ground floor...",
        "url": "https://www.etermin.net/international-office"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/es"
    },
    {
        "title": "Beratungstermin | Dr. Ines Kitzweger | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/kitzweger"
    },
    {
        "title": "Rahmer Dienstleistungen GmbH | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/rg"
    },
    {
        "title": "D\u00fcrener Autowaschcenter - Online Termin buchen",
        "url": "https://www.etermin.net/duerener-autowaschcenter"
    },
    {
        "title": "Medius - Zentrum f\u00fcr Gesundheit | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/medius"
    },
    {
        "title": "Praxis f\u00fcr klassische Hom\u00f6opathie - Adrian Schneider",
        "url": "https://www.etermin.net/homoeopathie-schneider"
    },
    {
        "title": "Corona Test Braunschweig | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/coronatestbs"
    },
    {
        "title": "G. Schaal GmbH - Online Termin buchen",
        "url": "https://www.etermin.net/schaal-terminbuchung"
    },
    {
        "title": "Testen Sie den eTermin Online Terminplaner 30 Tage kostenlos und...",
        "url": "https://www.etermin.net/registrieren"
    },
    {
        "title": "gerberCom.WERBEAGENTUR GmbH - Online Termin buchen",
        "url": "https://www.etermin.net/gerbercom"
    },
    {
        "title": "\u00d6sterreichische Gesundheitskasse | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/OEGK"
    },
    {
        "title": "Gesundheitsberuferegister Arbeiterkammer Salzburg",
        "url": "https://www.etermin.net/gbr"
    },
    {
        "title": "MEIN EU AUTO Wilhelm Nasaruk | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/eu-neuwagen"
    },
    {
        "title": "Autohaus Striesen Inh. Bernd Stegert | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/autohaus-striesen"
    },
    {
        "title": "Autohaus Holzberg | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/holzberg"
    },
    {
        "title": "Termin buchen | Wie m\u00f6chten Sie bezahlen?",
        "url": "https://www.etermin.net/sladkowski/"
    },
    {
        "title": "Hochsauerlandkreis | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/hsk-schnelltest"
    },
    {
        "title": "Praxis Sibylle Graf | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/osteopathie"
    },
    {
        "title": "Hebammenpraxis Rundum - Online Termin buchen",
        "url": "https://www.etermin.net/patriciaheld"
    },
    {
        "title": "Radhaus B\u00fcren GmbH Torsten Hieke | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/radhaus-bueren"
    },
    {
        "title": "il Aus- & Weiterbildung GmbH - Online Termin buchen",
        "url": "https://www.etermin.net/o/il-institut"
    },
    {
        "title": "Burwitz Legend\u00e4r Rostock | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/apries"
    },
    {
        "title": "Die Brillenmacher Leimen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/werner"
    },
    {
        "title": "Urologie am Marktplatz - Prof. Dr. med. Alexander Bachmann Aktuell...",
        "url": "https://www.etermin.net/swissurocenter"
    },
    {
        "title": "Testzentrum Hahnenklee - Online Termin buchen",
        "url": "https://www.etermin.net/testzentrumhahnenklee"
    },
    {
        "title": "Personalfirma HR DEMO Vorstellungsgespr\u00e4che",
        "url": "https://www.etermin.net/interview"
    },
    {
        "title": "Festwerk Unter den Eichen GmbH | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/festwerk-unter-den-eichen"
    },
    {
        "title": "hm-biovital - Online Termin buchen",
        "url": "https://www.etermin.net/hm-biovital"
    },
    {
        "title": "Buchen Sie jetzt Ihre Erstberatung bei uns online!",
        "url": "https://www.etermin.net/hollywoodpraxis/serviceid/149594?noinitscroll=1"
    },
    {
        "title": "Praxis DDr. Rainer Biedermann Kieferorthop\u00e4die",
        "url": "https://www.etermin.net/myo-dontix"
    },
    {
        "title": "Autohaus DEMO | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/reifen"
    },
    {
        "title": "Schnittstellen eTermin Online-Terminplaner zu anderen Anwendungen",
        "url": "https://www.etermin.net/online-terminbuchung-schnittstellen"
    },
    {
        "title": "Elementum Deutschland GmbH | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/elementum"
    },
    {
        "title": "Unternehmer Oberbayern Projekt der GWF Gesellschaft f\u00fcr Wirtschafts...",
        "url": "https://www.etermin.net/gwf-mbh"
    },
    {
        "title": "Digital.Solutions.Consulting - Online Termin buchen",
        "url": "https://www.etermin.net/termin"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/hoeffner-kuechenberatung?cr=teaser-k\u2026na&st=5032021&sz=470&prop=teaser-e-termin&ca=teaser-e-termin"
    },
    {
        "title": "Modehaus Vondru - Online Termin buchen",
        "url": "https://www.etermin.net/vondru"
    },
    {
        "title": "Stadt Coesfeld | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/coe/serviceid/165822"
    },
    {
        "title": "KANZLEI DR. SCHENK - Online Termin buchen",
        "url": "https://www.etermin.net/drschenk"
    },
    {
        "title": "Stadt Oberasbach | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtoberasbach"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/reginanevin"
    },
    {
        "title": "Burwitz Legend\u00e4r Schwerin | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/sduewiger"
    },
    {
        "title": "Termin buchen bei Rechtsanwalt J\u00fcrgen Sauerborn, Fachanwalt f\u00fcr...",
        "url": "https://www.etermin.net/sauerborn"
    },
    {
        "title": "Corona Testcenter | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/ASBTestcenter"
    },
    {
        "title": "\u00c4rztekammer f\u00fcr Wien | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/AerztekammerWien"
    },
    {
        "title": "Kammer f\u00fcr Arbeiter und Angestellte f\u00fcr das Burgenland",
        "url": "https://www.etermin.net/GBRBgld"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/Digital-Consulting"
    },
    {
        "title": "Renn und Bikesport | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/rubs"
    },
    {
        "title": "Online-Terminplaner und Online-Terminbuchung - eTermin",
        "url": "https://www.etermin.net/"
    },
    {
        "title": "hessenheizung - Terminbuchung | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/hessenheizung"
    },
    {
        "title": "Corona-Testcenter Hersfeld-Rotenburg - Online Termin buchen",
        "url": "https://www.etermin.net/testcenter-hef-rof"
    },
    {
        "title": "Staatsgalerie Stuttgart | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/staatsgalerie"
    },
    {
        "title": "Psychologische Studierendenberatung Innsbruck",
        "url": "https://www.etermin.net/PSB-Innsbruck"
    },
    {
        "title": "Ernst Klett Sprachen GmbH | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/EKS"
    },
    {
        "title": "Stadt Selm Online Terminkalender | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtselm"
    },
    {
        "title": "Termine bei DeSoCo buchen und verwalten",
        "url": "https://www.etermin.net/desoco/serviceid/57973"
    },
    {
        "title": "Navigierte Implantologie Wien | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/mtruppe"
    },
    {
        "title": "etheris M\u00fcnchen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/martinweitl"
    },
    {
        "title": "Kreis Steinfurt - Online Termin buchen",
        "url": "https://www.etermin.net/kreis-steinfurt"
    },
    {
        "title": "Universit\u00e4t Graz - Online Termin buchen",
        "url": "https://www.etermin.net/unitestet"
    },
    {
        "title": "Stadtgemeinde Schwechat - Online Termin buchen",
        "url": "https://www.etermin.net/schwechat"
    },
    {
        "title": "Marien Apotheke Wien | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/marienapowien"
    },
    {
        "title": "Dittrich N\u00e4hmaschinen - Online Termin buchen",
        "url": "https://www.etermin.net/dn_termine"
    },
    {
        "title": "Spitzweg Apotheke - Online Termin buchen",
        "url": "https://www.etermin.net/spitzweg-apotheke"
    },
    {
        "title": "Gm\u00fcr AG - Online Termin buchen",
        "url": "https://www.etermin.net/o/gmuer"
    },
    {
        "title": "Audi Zentrum F\u00fcrstenwalde - Online Termin buchen",
        "url": "https://www.etermin.net/audizentrum"
    },
    {
        "title": "Hundeschule DHK - Online Termin buchen",
        "url": "https://www.etermin.net/hundeschule-dhk"
    },
    {
        "title": "Wirbels\u00e4ulenzentrum Graz-Ragnitz - Online Termin buchen",
        "url": "https://www.etermin.net/wzg"
    },
    {
        "title": "Testzentrum Goslar | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/testzentrumgoslar"
    },
    {
        "title": "Verbandsgemeindeverwaltung Daun | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/vgdaun"
    },
    {
        "title": "PflegeLeicht GbR Testzentrum | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/PflegeLeicht"
    },
    {
        "title": "Besuchen Sie uns, wir pr\u00e4sentieren Ihnen unsere H\u00e4user ausf\u00fchrlich.",
        "url": "https://www.etermin.net/Besichtigungstermin"
    },
    {
        "title": "Online-Terminbuchung und Terminkalender von eTermin",
        "url": "https://www.etermin.net/online-terminbuchung"
    },
    {
        "title": "Jobcenter Bonn | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/jcbn"
    },
    {
        "title": "Arras Technische Schulungen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/bfs-staplerschein"
    },
    {
        "title": "Die Praxis - Online Termin buchen",
        "url": "https://www.etermin.net/die-praxis-bamberg"
    },
    {
        "title": "Abt. Br\u00fcckenbau | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/ST5"
    },
    {
        "title": "Corona-Schnellteststelle Teublitz - Online Termin buchen",
        "url": "https://www.etermin.net/spitzwegapo"
    },
    {
        "title": "Energie Graz GmbH & Co KG, Kundenservicecenter",
        "url": "https://www.etermin.net/egg"
    },
    {
        "title": "Kanzlei Grueneberg - Online Termin buchen",
        "url": "https://www.etermin.net/grueneberg"
    },
    {
        "title": "Stadt Graz | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stadtgraz?servicegroupid=66207"
    },
    {
        "title": "Gruppe Stra\u00dfe | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/ST1"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/noegkk"
    },
    {
        "title": "Gemeinde Stahnsdorf | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/stahnsdorf"
    },
    {
        "title": "Sch\u00fcnemann Augenoptik GmbH - Online Termin buchen",
        "url": "https://www.etermin.net/ms1"
    },
    {
        "title": "BVMW Wirtschaftsregion M\u00fcnchen | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/kb1"
    },
    {
        "title": "Gesundheit \u00d6sterreich GmbH - Gesundheitsberuferegister...",
        "url": "https://www.etermin.net/gesundheitsberuferegister"
    },
    {
        "title": "Praxisgemeinschaft Silima \u00c4rzte und Therapeuten der ehemaligen...",
        "url": "https://www.etermin.net/praxis-silima"
    },
    {
        "title": "RKT Rettungsdienst OHG | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/CoronaTestzentrum-RKT"
    },
    {
        "title": "Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/KIGA"
    },
    {
        "title": "Praxis f\u00fcr Osteopathie Dirk Kaiser | Der Termin wurde nicht gebucht!",
        "url": "https://www.etermin.net/praxiskaiser"
    },
    {
        "title": "Bezirkshauptmannschaft G\u00e4nserndorf - Online Termin buchen",
        "url": "https://www.etermin.net/Bezirkshauptmannschaft_Gaenserndorf"
    },
    {
        "title": "Termin buchen | Wie m\u00f6chten Sie bezahlen?",
        "url": "https://www.etermin.net/sladkowski/impressum"
    },
    {
        "title": "Corona TESTZENTRUM im Elithera Therapiezentrum Springe",
        "url": "https://www.etermin.net/testzentrum1"
    }
]


HAND_PICKED = [
    ("graz", "Stadt Graz", "stadtgraz"),
    ("lehrte", "Stadt Lehrte", "StadtLehrte"),
    ("billerbeck", "Stadt Billerbeck Verwaltung", "termininbillerbeck"),
    ("dormagen", "Stadt Dormagen", "stadtdormagen"),
    ("fuerth-test", "SARS-CoV-2 Testzentrum der Stadt Fürth", "Testzentrum_agnf"),
    ("butzbach", "Magistrat der Stadt Butzbach", "stadtbutzbach"),
    ("duelmen", "Stadt Dülmen", "duelmen"),
    ("halbersadt", "Stadt Halberstadt", "halberstadt"),
    ("stadtbergen", "Stadt Stadtbergen", "stadtbergen"),
    ("wiehl", "Stadt Wiehl", "stadtwiehl"),
    ("itzehoe", "Stadt Itzehoe Einwohnermeldeamt", "Stadt_Itzehoe"),
    ("grazamt", "BürgerInnenamt Stadt Graz", "buergerinnenamt"),
    ("ru1", "Abt. Bau- und Raumordnungsrecht" "ru1"),
    ("ru7", "Abt. Raumordnung und Gesamtverkehrsangelegenheiten", "ru7"),
    ("mittenwalde", "Stadt Mittenwalde", "StadtMittenwalde"),
    ("stuttgartpalais", "StadtPalais - Museum für Stuttgart", "stadtlaborstuttgart"),
    ("blankenburg", "Stadt Blankenburg (Harz)", "blankenburg"),
    ("wedemarktest", "Corona-Schnelltestzentrum Caspar & Dase für die Wedemark", "Schnelltestungen"),
    ("hammersbachtest", "Schnelltestzentrum Hammersbach", "Schnelltestzentrum"),
    ("baselgewerbe", "Wirtschaft unter Strom - Online Termin buchen", "gewerbe-basel"),
    ("bbmess", "Landesamt für Mess- und Eichwesen Berlin-Brandenburg", "lme-be-bb"),
    ("geldernsw", "Stadtwerke Geldern Netz", "Zaehlerwechseltermine"),
    ("weimarunioffice", "Bauhaus-Universität Weimar Erdgeschoss Raum 002", "international-office"),
    ("braunschweigtest", "Corona Test Braunschweig", "coronatestbs"),
    ("oesterreichgk", "Österreichische Gesundheitskasse", "OEGK"),
    ("saluburggbr", "Gesundheitsberuferegister Arbeiterkammer Salzburg", "gbr"),
    ("hsktest", "Hochsauerlandkreis", "hsk-schnelltest"),
    ("hahnenklee", "Testzentrum Hahnenklee", "testzentrumhahnenklee"),
    ("coesfeld", "Stadt Coesfeld", "coe"),
    ("oberasbach", "Stadt Oberasbach", "stadtoberasbach"),
    ("asbtest", "Corona Testcenter", "ASBTestcenter"),
    ("wienak", "Ärztekammer für Wien", "AerztekammerWien"),
    ("burgendlandkaa", "Kammer für Arbeiter und Angestellte für das Burgenland", "GBRBgld"),
    ("hersfeldtest", "Corona-Testcenter Hersfeld-Rotenburg", "testcenter-hef-rof"),
    ("innsbruckpsych", "Psychologische Studierendenberatung Innsbruck", "PSB-Innsbruck"),
    ("selm", "Stadt Selm", "stadtselm"),
    ("kreissteinfurt", "Kreis Steinfurt", "kreis-steinfurt"),
    ("graz-uni", "Universität Graz", "unitestet"),
    ("goslartest", "Testzentrum Goslar", "testzentrumgoslar"),
    ("daunvg", "Verbandsgemeindeverwaltung Daun", "vgdaun"),
    ("bonnjob", "Jobcenter Bonn", "jcbn"),
    # ("brueckenbau", "Abt. Brückenbau", "ST5"),  # http://www.noe.gv.at/noe/Kontakt-Landesverwaltung/Gruppe_Strasse.html
    ("teublitztest", "Corona-Schnellteststelle Teublitz", "spitzwegapo"),
    ("stahnsdorf", "Gemeinde Stahnsdorf", "stahnsdorf"),
    ("elitheratest", "Corona TESTZENTRUM im Elithera", "testzentrum1"),
]
