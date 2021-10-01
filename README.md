# public offices appointment schedule scraper

Hi there! Similar to the 
[free parking lots scraper](https://github.com/defgsus/parking-scraper/),
this code collects data of enormous importance! 

In the spirit of *e-governance* a couple of german cities decided 
to force every citizen to acquaint themselves with this internet thing
and require them to make appointments with, e.g., the resident's 
registration office through a web interface. For these offices, 
there is no *just-go-there-and-wait-till-you're-called* anymore. 
In fact, if you go there without the web-appointment, the
service staff usually barks and blusters in the well-known
german public office tone.  

Anyways! Now we have this internet thing going and it's not so hard to 
track the development of the office schedules through time. From that
data we can infer:

- the business of the offices over time (e.g. barking at foreigners)
- the desire of citizens to plan ahead (e.g. not taking the first
free slot but one in 4 weeks)
- the most popular time of day for appointments
- the most popular time of day for making appointments
- the cancellation rate 

And all of that for a couple of different cities for comparison. 
As stated earlier: data of enormous importance!

Data scraping started at around 2021-07-09 and is weekly exported
to the [office-schedule-data](https://github.com/defgsus/office-schedule-scraper/)
repository.

To collect data yourself:

```shell script
# install
git clone https://github.com/defgsus/office-schedule-scraper
cd office-schedule-scraper
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

# make a snapshot
python scraper.py snapshot -w <X> -p <Y>
# where <X> is the number of weeks to look ahead (defaults to 4)
# where <Y> is the number of parallel processes to run
```

Which leads to a lot of JSON files in the `snapshot` directory. 

Using [export.py](export.py), the data will be exported to compressed
bunches of CSV files as described in [office-schedule-data](https://github.com/defgsus/office-schedule-scraper/).


### List of implemented websites

Here's a list of websites that are scraped (compiled via `python scraper.py list`):

| name                                                     | scraper    | url                                                                                                                                                              |
|:---------------------------------------------------------|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Amt Kluetzer Winkel                                      | tevis      | [tevis-online.mvnet.de/kluetzerwinkel/](https://tevis-online.mvnet.de/kluetzerwinkel/)                                                                           |
| Bauhaus-Universität Weimar Erdgeschoss Raum 002          | etermin    | [www.etermin.net/international-office/](https://www.etermin.net/international-office/)                                                                           |
| BürgerInnenamt Stadt Graz                                | etermin    | [www.etermin.net/buergerinnenamt/](https://www.etermin.net/buergerinnenamt/)                                                                                     |
| Corona TESTZENTRUM im Elithera                           | etermin    | [www.etermin.net/testzentrum1/](https://www.etermin.net/testzentrum1/)                                                                                           |
| Corona Test Braunschweig                                 | etermin    | [www.etermin.net/coronatestbs/](https://www.etermin.net/coronatestbs/)                                                                                           |
| Corona Testcenter                                        | etermin    | [www.etermin.net/ASBTestcenter/](https://www.etermin.net/ASBTestcenter/)                                                                                         |
| Corona-Schnellteststelle Teublitz                        | etermin    | [www.etermin.net/spitzwegapo/](https://www.etermin.net/spitzwegapo/)                                                                                             |
| Corona-Schnelltestzentrum Caspar & Dase für die Wedemark | etermin    | [www.etermin.net/Schnelltestungen/](https://www.etermin.net/Schnelltestungen/)                                                                                   |
| Corona-Testcenter Hersfeld-Rotenburg                     | etermin    | [www.etermin.net/testcenter-hef-rof/](https://www.etermin.net/testcenter-hef-rof/)                                                                               |
| Gemeinde Gottmadingen                                    | tevis      | [termine-reservieren.de/termine/gottmadingen/](https://termine-reservieren.de/termine/gottmadingen/)                                                             |
| Gemeinde Stahnsdorf                                      | etermin    | [www.etermin.net/stahnsdorf/](https://www.etermin.net/stahnsdorf/)                                                                                               |
| Gesundheitsberuferegister Arbeiterkammer Salzburg        | etermin    | [www.etermin.net/gbr/](https://www.etermin.net/gbr/)                                                                                                             |
| Hansestadt Wismar                                        | tevis      | [tevis-online.mvnet.de/wismar/](https://tevis-online.mvnet.de/wismar/)                                                                                           |
| Hochsauerlandkreis                                       | etermin    | [www.etermin.net/hsk-schnelltest/](https://www.etermin.net/hsk-schnelltest/)                                                                                     |
| Ilm-Kreis                                                | tevis      | [tvweb.ilm-kreis.de/ilmkreis/](https://tvweb.ilm-kreis.de/ilmkreis/)                                                                                             |
| Impftermin Thüringen                                     | custom     | [www.impfen-thueringen.de/terminvergabe/](https://www.impfen-thueringen.de/terminvergabe/)                                                                       |
| Jobcenter Bonn                                           | etermin    | [www.etermin.net/jcbn/](https://www.etermin.net/jcbn/)                                                                                                           |
| Kammer für Arbeiter und Angestellte für das Burgenland   | etermin    | [www.etermin.net/GBRBgld/](https://www.etermin.net/GBRBgld/)                                                                                                     |
| Kfz Zulassungstelle Grasbrunn                            | tevis      | [termine-reservieren.de/termine/lramuenchen/kfz-zulassungsstelle-grasbrunn/](https://termine-reservieren.de/termine/lramuenchen/kfz-zulassungsstelle-grasbrunn/) |
| Kiel Einwohnermeldeamt                                   | tevis      | [terminvergabe-ema-zulassung.kiel.de/tevisema/](https://terminvergabe-ema-zulassung.kiel.de/tevisema/)                                                           |
| Kreis Bergstraße                                         | netappoint | [terminreservierungverkehr.kreis-bergstrasse.de/netappoint/...](https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint/index.php?company=bergstrasse) |
| Kreis Coesfeld                                           | etermin    | [www.etermin.net/kreiscoesfeld/](https://www.etermin.net/kreiscoesfeld/)                                                                                         |
| Kreis Germersheim Kfz-Zulassungsbehörde                  | netappoint | [kfz.kreis-germersheim.de/netappoint/...](https://kfz.kreis-germersheim.de/netappoint/index.php?company=kreis-germersheim)                                       |
| Kreis Groß-Gerau                                         | tevis      | [tevis.ekom21.de/grg/](https://tevis.ekom21.de/grg/)                                                                                                             |
| Kreis Ludwigshfen                                        | tevis      | [tevisweb.ludwigshafen.de/](https://tevisweb.ludwigshafen.de/)                                                                                                   |
| Kreis Soest                                              | tevis      | [termine-buergerdienste.kreis-soest.de/](https://termine-buergerdienste.kreis-soest.de/)                                                                         |
| Kreis Steinfurt                                          | etermin    | [www.etermin.net/kreis-steinfurt/](https://www.etermin.net/kreis-steinfurt/)                                                                                     |
| Kreis Wesel                                              | tevis      | [tevis.krzn.de/tevisweb080/](https://tevis.krzn.de/tevisweb080/)                                                                                                 |
| Landesamt für Mess- und Eichwesen Berlin-Brandenburg     | etermin    | [www.etermin.net/lme-be-bb/](https://www.etermin.net/lme-be-bb/)                                                                                                 |
| Landkreis Bernkastel-Wittlich                            | tevis      | [termine-reservieren.de/termine/bernkastel-wittlich/](https://termine-reservieren.de/termine/bernkastel-wittlich/)                                               |
| Landkreis Breisgau-Hochschwarzwald Kfz-Zulassungsbehörde | netappoint | [termin.lkbh.net/...](https://termin.lkbh.net/index.php?company=lkbh-zulassung)                                                                                  |
| Landkreis Breisgau-Hochschwarzwald Landwitschaft         | netappoint | [termin.lkbh.net/...](https://termin.lkbh.net/index.php?company=lkbh-lw)                                                                                         |
| Landkreis Cochem-Zell                                    | tevis      | [termine-reservieren.de/termine/cochem-zell/](https://termine-reservieren.de/termine/cochem-zell/)                                                               |
| Landkreis Friesland                                      | tevis      | [onlinetermine.friesland.de/](https://onlinetermine.friesland.de/)                                                                                               |
| Landkreis Goeppingen                                     | tevis      | [termin.landkreis-goeppingen.de/](https://termin.landkreis-goeppingen.de/)                                                                                       |
| Landkreis Mayen-Koblenz                                  | tevis      | [termine-reservieren.de/termine/kvmayen-koblenz/](https://termine-reservieren.de/termine/kvmayen-koblenz/)                                                       |
| Landkreis München Ausländerbehörde                       | tevis      | [termine-reservieren.de/termine/lramuenchen/auslaenderbehoerde/](https://termine-reservieren.de/termine/lramuenchen/auslaenderbehoerde/)                         |
| Landkreis München Jobcenter                              | tevis      | [amtonline.de/tvweb/jc-muenchen/](https://amtonline.de/tvweb/jc-muenchen/)                                                                                       |
| Landkreis Ortenau                                        | tevis      | [www.termine.lraog.de/](https://www.termine.lraog.de/)                                                                                                           |
| Landkreis Stade                                          | tevis      | [termine-reservieren.de/termine/stade/](https://termine-reservieren.de/termine/stade/)                                                                           |
| Landkreis Verden                                         | tevis      | [lkv.landkreis-verden.de/TEVISWEB/](https://lkv.landkreis-verden.de/TEVISWEB/)                                                                                   |
| Landkreis Weilheim-Schongau                              | tevis      | [termine-reservieren.de/termine/weilheimschongau/](https://termine-reservieren.de/termine/weilheimschongau/)                                                     |
| Landkreis Zwickau                                        | tevis      | [termine-reservieren.de/termine/lra-zwickau/](https://termine-reservieren.de/termine/lra-zwickau/)                                                               |
| Landratsamt Dachau                                       | tevis      | [termine.landratsamt-dachau.de/tevis/](https://termine.landratsamt-dachau.de/tevis/)                                                                             |
| Landratsamt Deggendorf                                   | etermin    | [www.etermin.net/LRA-DEG-Termin/](https://www.etermin.net/LRA-DEG-Termin/)                                                                                       |
| Landratsamt Fürstenfeldbruck                             | tevis      | [termine-reservieren.de/termine/lra-ffb/](https://termine-reservieren.de/termine/lra-ffb/)                                                                       |
| Landratsamt Miesbach                                     | tevis      | [termine-reservieren.de/termine/lra-miesbach/](https://termine-reservieren.de/termine/lra-miesbach/)                                                             |
| Landratsamt München                                      | tevis      | [termine-reservieren.de/termine/lramuenchen/efa/](https://termine-reservieren.de/termine/lramuenchen/efa/)                                                       |
| Magistrat der Stadt Butzbach                             | etermin    | [www.etermin.net/stadtbutzbach/](https://www.etermin.net/stadtbutzbach/)                                                                                         |
| Märkischer Kreis                                         | tevis      | [terminvergabe.maerkischer-kreis.de/](https://terminvergabe.maerkischer-kreis.de/)                                                                               |
| Psychologische Studierendenberatung Innsbruck            | etermin    | [www.etermin.net/PSB-Innsbruck/](https://www.etermin.net/PSB-Innsbruck/)                                                                                         |
| SARS-CoV-2 Testzentrum der Stadt Fürth                   | etermin    | [www.etermin.net/Testzentrum_agnf/](https://www.etermin.net/Testzentrum_agnf/)                                                                                   |
| Salzlandkreis                                            | tevis      | [termine.salzlandkreis.de/](https://termine.salzlandkreis.de/)                                                                                                   |
| Schnelltestzentrum Hammersbach                           | etermin    | [www.etermin.net/Schnelltestzentrum/](https://www.etermin.net/Schnelltestzentrum/)                                                                               |
| Stadt Amberg                                             | tevis      | [termine.amberg.de/](https://termine.amberg.de/)                                                                                                                 |
| Stadt Bad-Kreuznach                                      | tevis      | [termine-reservieren.de/termine/svkh/](https://termine-reservieren.de/termine/svkh/)                                                                             |
| Stadt Billerbeck Verwaltung                              | etermin    | [www.etermin.net/termininbillerbeck/](https://www.etermin.net/termininbillerbeck/)                                                                               |
| Stadt Blankenburg (Harz)                                 | etermin    | [www.etermin.net/blankenburg/](https://www.etermin.net/blankenburg/)                                                                                             |
| Stadt Bochum Baubürgeramt                                | netappoint | [terminvergabe.bochum.de/...](https://terminvergabe.bochum.de/index.php?company=bochumbaub)                                                                      |
| Stadt Bochum Büro für Kfz-Angelegenheiten                | netappoint | [terminvergabe.bochum.de/...](https://terminvergabe.bochum.de/index.php?company=bochumbb)                                                                        |
| Stadt Bochum Zulassungsstelle                            | netappoint | [terminvergabe.bochum.de/...](https://terminvergabe.bochum.de/index.php?company=bochum-stva)                                                                     |
| Stadt Bochum Zulassungsstelle Umtausch                   | netappoint | [terminvergabe.bochum.de/...](https://terminvergabe.bochum.de/index.php?company=bochum-stva)                                                                     |
| Stadt Bonn                                               | netappoint | [onlinetermine.bonn.de/...](https://onlinetermine.bonn.de/index.php?company=stadtbonn)                                                                           |
| Stadt Bonn Bauamt                                        | netappoint | [onlinetermine.bonn.de/...](https://onlinetermine.bonn.de/index.php?company=stadtbonn-bau)                                                                       |
| Stadt Braunschweig                                       | netappoint | [otr.braunschweig.de/netappoint/...](https://otr.braunschweig.de/netappoint/index.php?company=stadtbraunschweig)                                                 |
| Stadt Bremen / Bremerhaven                               | tevis      | [termin.bremen.de/termine/](https://termin.bremen.de/termine/)                                                                                                   |
| Stadt Coesfeld                                           | etermin    | [www.etermin.net/coe/](https://www.etermin.net/coe/)                                                                                                             |
| Stadt Dormagen                                           | etermin    | [www.etermin.net/stadtdormagen/](https://www.etermin.net/stadtdormagen/)                                                                                         |
| Stadt Dresden                                            | netappoint | [termine.dresden.de/netappoint/...](https://termine.dresden.de/netappoint/index.php?company=stadtdresden-fs)                                                     |
| Stadt Dresden Kfz-Zulassungsbehörde                      | netappoint | [termine.dresden.de/netappoint/...](https://termine.dresden.de/netappoint/index.php?company=stadtdresden-kfz)                                                    |
| Stadt Dülmen                                             | etermin    | [www.etermin.net/duelmen/](https://www.etermin.net/duelmen/)                                                                                                     |
| Stadt Egelsbach                                          | tevis      | [tevis.ekom21.de/egb/](https://tevis.ekom21.de/egb/)                                                                                                             |
| Stadt Eislingen                                          | tevis      | [termine-reservieren.de/termine/eislingen/](https://termine-reservieren.de/termine/eislingen/)                                                                   |
| Stadt Frankenthal                                        | tevis      | [termine-reservieren.de/termine/frankenthal/](https://termine-reservieren.de/termine/frankenthal/)                                                               |
| Stadt Frankfurt                                          | tevis      | [tevis.ekom21.de/fra/](https://tevis.ekom21.de/fra/)                                                                                                             |
| Stadt Friedrichsdorf                                     | tevis      | [tevis.ekom21.de/frf/](https://tevis.ekom21.de/frf/)                                                                                                             |
| Stadt Fulda                                              | tevis      | [termine-reservieren.de/termine/fulda/](https://termine-reservieren.de/termine/fulda/)                                                                           |
| Stadt Graz                                               | etermin    | [www.etermin.net/stadtgraz/](https://www.etermin.net/stadtgraz/)                                                                                                 |
| Stadt Greifswald                                         | tevis      | [tevis-online.mvnet.de/greifswald/](https://tevis-online.mvnet.de/greifswald/)                                                                                   |
| Stadt Gronau                                             | tevis      | [termine-reservieren.de/termine/gronau/](https://termine-reservieren.de/termine/gronau/)                                                                         |
| Stadt Groß-Umstadt                                       | tevis      | [tevis.ekom21.de/gad/](https://tevis.ekom21.de/gad/)                                                                                                             |
| Stadt Göttingen                                          | tevis      | [termin.goettingen.de/](https://termin.goettingen.de/)                                                                                                           |
| Stadt Halberstadt                                        | etermin    | [www.etermin.net/halberstadt/](https://www.etermin.net/halberstadt/)                                                                                             |
| Stadt Halle                                              | netappoint | [ncu.halle.de/...](https://ncu.halle.de/index.php?company=stadthalle)                                                                                            |
| Stadt Heidelberg                                         | tevis      | [tevis-online.heidelberg.de/](https://tevis-online.heidelberg.de/)                                                                                               |
| Stadt Hof                                                | tevis      | [termine-reservieren.de/termine/hof/](https://termine-reservieren.de/termine/hof/)                                                                               |
| Stadt Hornberg                                           | tevis      | [tevis.ekom21.de/hbe/](https://tevis.ekom21.de/hbe/)                                                                                                             |
| Stadt Hünstetten                                         | tevis      | [tevis.ekom21.de/hsz/](https://tevis.ekom21.de/hsz/)                                                                                                             |
| Stadt Hüttenberg                                         | tevis      | [tevis.ekom21.de/htb/](https://tevis.ekom21.de/htb/)                                                                                                             |
| Stadt Ingelheim                                          | tevis      | [termine-reservieren.de/termine/ingelheim/](https://termine-reservieren.de/termine/ingelheim/)                                                                   |
| Stadt Itzehoe Einwohnermeldeamt                          | etermin    | [www.etermin.net/Stadt_Itzehoe/](https://www.etermin.net/Stadt_Itzehoe/)                                                                                         |
| Stadt Jena                                               | tevis      | [tevis-bs.jena.de/](https://tevis-bs.jena.de/)                                                                                                                   |
| Stadt Kaiserslautern Ausländerbehörde                    | netappoint | [www3.kaiserslautern.de/netappoint/...](https://www3.kaiserslautern.de/netappoint/index.php?company=kaiserslautern-ausl)                                         |
| Stadt Kassel                                             | tevis      | [tevis.ekom21.de/kas/](https://tevis.ekom21.de/kas/)                                                                                                             |
| Stadt Kelsterbach                                        | tevis      | [tevis.ekom21.de/keb/](https://tevis.ekom21.de/keb/)                                                                                                             |
| Stadt Koeln                                              | netappoint | [termine-online.stadt-koeln.de/...](https://termine-online.stadt-koeln.de/index.php?company=stadtkoeln)                                                          |
| Stadt Lehrte                                             | etermin    | [www.etermin.net/StadtLehrte/](https://www.etermin.net/StadtLehrte/)                                                                                             |
| Stadt Leipzig                                            | custom     | [leipzig.de/fachanwendungen/termine/...](https://leipzig.de/fachanwendungen/termine/index.html)                                                                  |
| Stadt Leipzig Standesamt                                 | netappoint | [adressen.leipzig.de/netappoint/...](https://adressen.leipzig.de/netappoint/index.php?company=leipzig-standesamt)                                                |
| Stadt Leun                                               | tevis      | [tevis.ekom21.de/lnx/](https://tevis.ekom21.de/lnx/)                                                                                                             |
| Stadt Linsengericht                                      | tevis      | [tevis.ekom21.de/lsg/](https://tevis.ekom21.de/lsg/)                                                                                                             |
| Stadt Löhne                                              | tevis      | [termine-reservieren.de/termine/loehne/](https://termine-reservieren.de/termine/loehne/)                                                                         |
| Stadt Magdeburg                                          | netappoint | [service.magdeburg.de/netappoint/...](https://service.magdeburg.de/netappoint/index.php?company=magdeburg)                                                       |
| Stadt Mainz                                              | tevis      | [otv.mainz.de/](https://otv.mainz.de/)                                                                                                                           |
| Stadt Mechernich                                         | tevis      | [amtonline.de/tvweb/mechernich/](https://amtonline.de/tvweb/mechernich/)                                                                                         |
| Stadt Minden                                             | tevis      | [termine-reservieren.de/termine/minden/](https://termine-reservieren.de/termine/minden/)                                                                         |
| Stadt Mittenwalde                                        | etermin    | [www.etermin.net/StadtMittenwalde/](https://www.etermin.net/StadtMittenwalde/)                                                                                   |
| Stadt Muenster                                           | tevis      | [termine.stadt-muenster.de/](https://termine.stadt-muenster.de/)                                                                                                 |
| Stadt Mörlenbach                                         | tevis      | [tevis.ekom21.de/mah/](https://tevis.ekom21.de/mah/)                                                                                                             |
| Stadt Mülheim an der Ruhr                                | tevis      | [terminvergabe.muelheim-ruhr.de/](https://terminvergabe.muelheim-ruhr.de/)                                                                                       |
| Stadt Neu-Isenburg                                       | tevis      | [tevis.ekom21.de/nis/](https://tevis.ekom21.de/nis/)                                                                                                             |
| Stadt Niedenstein                                        | tevis      | [tevis.ekom21.de/nsn/](https://tevis.ekom21.de/nsn/)                                                                                                             |
| Stadt Nordhausen                                         | tevis      | [tevis.svndh.de/](https://tevis.svndh.de/)                                                                                                                       |
| Stadt Nürnberg                                           | tevis      | [nuernberg.termine-reservieren.de/](https://nuernberg.termine-reservieren.de/)                                                                                   |
| Stadt Ober-Ramstadt                                      | tevis      | [tevis.ekom21.de/oby/](https://tevis.ekom21.de/oby/)                                                                                                             |
| Stadt Oberasbach                                         | etermin    | [www.etermin.net/stadtoberasbach/](https://www.etermin.net/stadtoberasbach/)                                                                                     |
| Stadt Offenbach                                          | tevis      | [tevis.ekom21.de/off/](https://tevis.ekom21.de/off/)                                                                                                             |
| Stadt Olfen                                              | etermin    | [www.etermin.net/stadtolfen/](https://www.etermin.net/stadtolfen/)                                                                                               |
| Stadt Paderborn                                          | tevis      | [termine-reservieren.de/termine/paderborn/](https://termine-reservieren.de/termine/paderborn/)                                                                   |
| Stadt Pfungstadt                                         | tevis      | [tevis.ekom21.de/pft/](https://tevis.ekom21.de/pft/)                                                                                                             |
| Stadt Radolfzell                                         | tevis      | [amtonline.de/tvweb/radolfzell/](https://amtonline.de/tvweb/radolfzell/)                                                                                         |
| Stadt Rastatt                                            | tevis      | [termine-reservieren.de/termine/rastatt/](https://termine-reservieren.de/termine/rastatt/)                                                                       |
| Stadt Saarbrücken                                        | tevis      | [terminvergabe.saarbruecken.de/](https://terminvergabe.saarbruecken.de/)                                                                                         |
| Stadt Salzgitter                                         | tevis      | [termine-reservieren.de/termine/salzgitter/](https://termine-reservieren.de/termine/salzgitter/)                                                                 |
| Stadt Schönebeck (Elbe)                                  | tevis      | [termine-reservieren.de/termine/schoenebeck-elbe/](https://termine-reservieren.de/termine/schoenebeck-elbe/)                                                     |
| Stadt Selm                                               | etermin    | [www.etermin.net/stadtselm/](https://www.etermin.net/stadtselm/)                                                                                                 |
| Stadt Speyer                                             | tevis      | [termine-reservieren.de/termine/speyer/](https://termine-reservieren.de/termine/speyer/)                                                                         |
| Stadt Stadtbergen                                        | etermin    | [www.etermin.net/stadtbergen/](https://www.etermin.net/stadtbergen/)                                                                                             |
| Stadt Steinburg                                          | tevis      | [termine-reservieren.de/termine/steinburg/](https://termine-reservieren.de/termine/steinburg/)                                                                   |
| Stadt Söst                                               | tevis      | [termine-reservieren.de/termine/stadtsoest/](https://termine-reservieren.de/termine/stadtsoest/)                                                                 |
| Stadt Trier                                              | tevis      | [termine-reservieren.de/termine/trier/](https://termine-reservieren.de/termine/trier/)                                                                           |
| Stadt Unna                                               | tevis      | [termine-reservieren.de/termine/unna/](https://termine-reservieren.de/termine/unna/)                                                                             |
| Stadt Viernheim                                          | tevis      | [tevis.ekom21.de/vhx/](https://tevis.ekom21.de/vhx/)                                                                                                             |
| Stadt Walldorf                                           | etermin    | [www.etermin.net/stadt-walldorf/](https://www.etermin.net/stadt-walldorf/)                                                                                       |
| Stadt Weimar                                             | tevis      | [tevis.weimar.de/](https://tevis.weimar.de/)                                                                                                                     |
| Stadt Weiterstadt                                        | tevis      | [tevis.ekom21.de/wdt/](https://tevis.ekom21.de/wdt/)                                                                                                             |
| Stadt Wiehl                                              | etermin    | [www.etermin.net/stadtwiehl/](https://www.etermin.net/stadtwiehl/)                                                                                               |
| Stadt Wittmund                                           | tevis      | [termine-reservieren.de/termine/wittmund/stva/](https://termine-reservieren.de/termine/wittmund/stva/)                                                           |
| Stadt Worms                                              | tevis      | [termine-reservieren.de/termine/worms/](https://termine-reservieren.de/termine/worms/)                                                                           |
| StadtPalais - Museum für Stuttgart                       | etermin    | [www.etermin.net/stadtlaborstuttgart/](https://www.etermin.net/stadtlaborstuttgart/)                                                                             |
| Stadtwerke Geldern Netz                                  | etermin    | [www.etermin.net/Zaehlerwechseltermine/](https://www.etermin.net/Zaehlerwechseltermine/)                                                                         |
| Städteregion Aachen                                      | netappoint | [terminmanagement.regioit-aachen.de/sr_aachen/...](https://terminmanagement.regioit-aachen.de/sr_aachen/index.php?company=staedteregion-aachen)                  |
| Testzentrum Goslar                                       | etermin    | [www.etermin.net/testzentrumgoslar/](https://www.etermin.net/testzentrumgoslar/)                                                                                 |
| Testzentrum Hahnenklee                                   | etermin    | [www.etermin.net/testzentrumhahnenklee/](https://www.etermin.net/testzentrumhahnenklee/)                                                                         |
| Universität Graz                                         | etermin    | [www.etermin.net/unitestet/](https://www.etermin.net/unitestet/)                                                                                                 |
| Verbandsgemeindeverwaltung Daun                          | etermin    | [www.etermin.net/vgdaun/](https://www.etermin.net/vgdaun/)                                                                                                       |
| Zulassungsstelle Leverkusen                              | netappoint | [termine.leverkusen.de/...](https://termine.leverkusen.de/index.php?company=LEV-Zulassung)                                                                       |
| Österreichische Gesundheitskasse                         | etermin    | [www.etermin.net/OEGK/](https://www.etermin.net/OEGK/)                                                                                                           |

The scraped interfaces which are used by most websites:

- **tevis**: https://www.kommunix.de/produkte/tevis/
- **netappoint**: http://www.edv-kahlert.de/produkte/Netcallup/netalarmpro1.htm
- **etermin**: https://www.etermin.net/  


### Data details

At each **snapshot** all **available dates** are recorded for each listed 
office department. The **tevis** system shows the available dates for
the next **N** full weeks, where **N** is set to **6** in my recording job.
The **etermin** and **netappoint** system is asked for the next **N** * 7 days.
 
Here's an example for one day from the 
[website of **Bonn**](https://onlinetermine.bonn.de/index.php?company=stadtbonn):

|                     | *Führerscheinwesen* | *Kfz-Zulassungswesen* | *Meldewesen* |
|:--------------------|:--------------------|:----------------------|:-------------|
| 2021-08-10T07:45:00 |                     | X                     |              |
| 2021-08-10T07:50:00 |                     | X                     |              |
| 2021-08-10T07:55:00 | X                   | X                     |              |
| 2021-08-10T08:00:00 | X                   | X                     |              |
| 2021-08-10T08:05:00 | X                   | X                     |              |
| 2021-08-10T08:10:00 | X                   | X                     |              |
| 2021-08-10T08:15:00 | X                   | X                     |              |
| 2021-08-10T08:20:00 | X                   | X                     |              |
| 2021-08-10T08:25:00 | X                   | X                     |              |
| 2021-08-10T08:30:00 | X                   | X                     |              |
| 2021-08-10T08:35:00 | X                   | X                     |              |
| 2021-08-10T08:40:00 | X                   | X                     |              |
| 2021-08-10T08:45:00 | X                   | X                     |              |
| 2021-08-10T08:50:00 | X                   | X                     |              |
| 2021-08-10T08:55:00 | X                   | X                     |              |
| 2021-08-10T09:00:00 |                     | X                     |              |
| 2021-08-10T09:05:00 |                     | X                     |              |
| 2021-08-10T09:10:00 |                     | X                     |              |
| 2021-08-10T09:15:00 | X                   | X                     |              |
| 2021-08-10T09:20:00 | X                   | X                     |              |
| 2021-08-10T09:25:00 | X                   | X                     |              |
| 2021-08-10T09:30:00 | X                   | X                     |              |
| 2021-08-10T09:35:00 | X                   | X                     |              |
| 2021-08-10T09:40:00 | X                   | X                     |              |
| 2021-08-10T09:45:00 | X                   | X                     |              |
| 2021-08-10T09:50:00 | X                   | X                     |              |
| 2021-08-10T09:55:00 | X                   | X                     |              |
| 2021-08-10T10:00:00 |                     | X                     |              |
| 2021-08-10T10:05:00 |                     | X                     |              |
| 2021-08-10T10:10:00 |                     | X                     |              |
| 2021-08-10T10:15:00 |                     | X                     |              |
| 2021-08-10T10:20:00 | X                   | X                     |              |
| 2021-08-10T10:25:00 | X                   | X                     |              |
| 2021-08-10T10:30:00 |                     | X                     |              |
| 2021-08-10T10:35:00 |                     | X                     |              |
| 2021-08-10T10:40:00 |                     | X                     |              |
| 2021-08-10T10:45:00 |                     | X                     |              |
| 2021-08-10T10:50:00 | X                   | X                     |              |
| 2021-08-10T10:55:00 | X                   | X                     |              |
| 2021-08-10T11:00:00 |                     | X                     |              |
| 2021-08-10T11:05:00 |                     | X                     |              |
| 2021-08-10T11:10:00 | X                   | X                     |              |
| 2021-08-10T11:15:00 | X                   | X                     |              |
| 2021-08-10T11:20:00 | X                   | X                     |              |
| 2021-08-10T11:25:00 | X                   | X                     |              |
| 2021-08-10T11:30:00 | X                   | X                     |              |
| 2021-08-10T11:35:00 | X                   | X                     |              |
| 2021-08-10T11:40:00 | X                   | X                     |              |
| 2021-08-10T11:45:00 | X                   | X                     |              |
| 2021-08-10T11:50:00 | X                   | X                     |              |
| 2021-08-10T11:55:00 | X                   | X                     |              |
| 2021-08-10T12:00:00 |                     | X                     |              |
| 2021-08-10T12:05:00 |                     | X                     |              |
| 2021-08-10T12:10:00 |                     | X                     |              |
| 2021-08-10T12:15:00 | X                   | X                     |              |
| 2021-08-10T12:20:00 | X                   | X                     |              |
| 2021-08-10T12:25:00 |                     | X                     |              |
| 2021-08-10T12:30:00 | X                   |                       |              |
| 2021-08-10T12:35:00 | X                   |                       |              |
| 2021-08-10T12:40:00 | X                   |                       |              |

Obviously they offer 5 minute slots and, yes, german offices might
close quite early. By looking at more data one can see
that *Meldewesen* and *Führerscheinwesen* exchange availability between weeks. 

It's not possible for all websites/systems to gather the actual business
hours for each day so a single snapshot is not necessarily enough to
calculate the correct number of appointments for each day. 

However, when comparing
two successive snapshots, it's possible to count new appointments or 
cancellations *quite* robustly and then attach a timestamp of when the 
appointments where made, clicked or activated or however this is called.

Still, there seem to be some erratic updates which mess up the calculation
and some offices seem to only update the availability every couple of days. 
In fact, this project turned out to demand **a lot** of time and work, 
especially in finding and fixing all my mistakes in the beginning. 
After the first 10 weeks of data collection, some of the mistakes have
been spotted.  

Below's a week of extracted data for all netappoint/tevis interfaces
resampled to a 1 hour interval. Offices with strange peaks where
excluded.  

![timeline through one week](/docs/one-week-all.png)

Blue line is number of appointments
and red line is cancellations.

One custom appointment interface of special interest is the 
[Impf-Terminvergabe Thüringen](https://www.impfen-thueringen.de/terminvergabe/index.php),
the website to make covid vaccination appointments in Thuringia.
They only offer one timeslot per day for at most 3 different days.
And their offered dates change all the time. Out of pure interest,
a snapshot is recorded every minute! 

In below graphic, whenever a new snapshot
offers a timeslot that is **after** the previously offered timeslot,
the previous timeslot is counted as one appointment.

![timeline through one week for vaccination](/docs/one-week-vacc.png) 

These are probably not real appointments but rather 
a measure of website activity as the total number of appointments made
would be over 190,000 in a period of 10 days. That does not really
fit the perceived reality.


### TODO-list of websites i found

- *"QMatic"* 
    - https://terminonline.neubrandenburg.de/netappoint/index.php?option=showbooking&company=neubrandenburg&cur_cause=1&auth=&month=06&year=2021&sel=8
      
      They seem to have an older (or newer?) version of netappoint belonging to netcallup.de/qmatic
    - https://www.lra-aoe.de/qmaticwebbooking/#/ some other qmatic page..
    - https://www.qtermin.de/A36-Kalender-Monschau
    - https://www.qtermin.de/mtk-gesundheitsamt
    - https://www.qtermin.de/mtk-sva
    - https://onlinetermin.mtk.org/qmaticwebbooking/#/preselect/branch/6e2377dedb49f2593139afc7f9e12abcb813995ff7e7ae3a86278d40749d266d
    - https://www.qtermin.de/mtk-jugendamt
    - https://onlinetermin.mtk.org/qmaticwebbooking/#/preselect/branch/998463c90b4d5c14787e84e162de4af0f584f1a59460f7a3d8b00c1ec686d827
    - https://www.qtermin.de/stadt-duisburg-zul
    - https://www.qtermin.de/qtermin-stadt-freiburg-bs
    
- https://www.kreis-alzey-worms.eu/verwaltung/zulassungsstelle/buchung/terminbuchung.php

  Quite simple XHR interface

- https://aufrufanlage36.bottrop.de/?

- https://eservice01.kreis-calw.de/

- https://sean.outsystemsenterprise.com/TicketSystemOnlineTermine/

- https://terminreservierung.blutspende.de/

- https://scheduler.mobimed.at/kinemedic/

- timeacle.com
    - https://timeacle.com/business/index/id/374 (Braunschweig)
    - https://timeacle.com/business/index/id/3134/booking/appointment/row_id/undefined/ (Oldenburg)
    - https://timeacle.com/business/index/id/2329/booking/appointment/row_id/3238
    - https://timeacle.com/business/index/id/2339/booking/appointment/row_id/3278
    
- https://spieleland.besuchsplaner.online

- https://meintermin.essen.de/termine/index.php

- https://testtermin.de/ - corona tests across germany

- https://www.rhein-erft-kreis.de/artikel/termine-online-reservieren

- Another generic appointment service by www.cleverq.de (Business Intelligent Cloud GmbH)
    - https://cqm.cleverq.de/public/appointments/lk_cloppenpurg_kfz_cloppenburg/index.html?lang=de
    - https://cqm.cleverq.de/public/appointments/zulassung_alzenau/index.html?lang=de 
    - https://cqm.cleverq.de/public/appointments/Zulassung-Segeberg/index.html?lang=de
    - https://cqm.cleverq.de/public/appointments/norderstedt/index.html?lang=de
    
- https://tempus-termine.com/termine/index.php?anlagennr=12 (by Berner Telecom-Dienste - Wuppertal.) 
  
  By searching through the ids, they seem to have maybe 40 real offices behind. 
  Unfortunately there's no json and many pages are styled or made 
  differently. Would be a good deal of work..

- https://www.buergerserviceportal.de/

  They require registration.

- *Smart Customer eXperience* https://smart-cjm.com
    - https://rsk.saas.smartcjm.com/m/strassenverkehrsamt/extern/calendar/?uid=8a08422a-9d05-48e4-bb31-4ee51c4cd68a
    - https://termin.ostallgaeu.de/m/lra-oal/extern/calendar/?uid=259bec4f-6d28-46e3-a008-94818c84fe32
    - https://lk-biberach.saas.smartcjm.com/m/Zulassung/extern/calendar/?uid=0413567e-ad7b-46f8-abc0-d1756c39109c
    - https://termine.landkreis-karlsruhe.de/m/Zulassung/extern/calendar/?uid=81ebbc74-3681-4900-84e7-457ade4662ec
    - https://termin.kreis-oh.de/m/kreis-ostholstein/extern/calendar/?uid=e236b01b-460e-4c76-88db-7e083557c438&wsid=c262c86a-9973-4760-806a-bc9c75755014&lang=de
    - https://termine.lkgi.de/m/zulassungsstelle/extern/calendar/?uid=46c3c125-ee61-4949-97f4-132979349815
    - https://termine.lkgi.de/m/Zulassungstelle-Gruenberg/extern/calendar/?uid=36f4d860-a5e2-4f73-ad7c-6ee3619d3ff9
    - https://termine.lra-es.de/m/strassenverkehrsamt/extern/calendar/?uid=396fc9d8-b0e0-4138-8ab3-82bad96cdb3e
    - a couple linked on https://www.karlsruhe.de/b4/buergerdienste/terminvereinbarung.de
    - https://thor.ostalbkreis.de/m/oakstrassenverkehr/extern/calendar/?uid=caa33f31-2148-4149-986b-183dda71bdc3
    - https://termin.kreis-oh.de/m/kreis-ostholstein/extern/calendar/?uid=e236b01b-460e-4c76-88db-7e083557c438
    - https://termine.landkreis-guenzburg.de/m/lbb/extern/calendar/?uid=2224a191-d0b2-4432-aeae-ba69b10d03ba
    - https://emergency.saas.smartcjm.com/m/Stadtverwaltung-Langen/extern/calendar/?uid=c3bf3b96-7847-497f-a2f4-6d72a992890f&lang=de
    - https://emergency.saas.smartcjm.com/m/Stadtverwaltung-Langen/extern/calendar/?uid=cf6c0a32-6d3f-448b-a5fa-656aaa525715&lang=de
    - https://termine.bochum.de/m/buergerbuero/extern/calendar/?uid=eab3c2ce-bd9c-4c81-8dab-663aebdc0ce3
    - https://termine.bochum.de/m/standesamt/extern/calendar/?uid=8e909dba-a24a-4d55-b06b-a9dd0fed1cc6
    - https://termine.bochum.de/m/abuero/extern/calendar/?uid=c5829d01-0a37-4ed5-868b-16b2788265d6
    - https://termine.bochum.de/m/abuero/extern/calendar/?uid=404bfc07-3614-46fc-9f3a-801fb1fd8954
    - https://termine.kreislippe.de/m/kreis-lippe/extern/calendar/?uid=b19ec13c-2d76-4188-a3e2-d63d6d2567c6
    - https://lk-suedliche-weinstrasse.saas.smartcjm.com/m/sva/extern/calendar/?uid=824ff5f9-7e19-40ef-ba08-c3837cb05d79
    - https://lk-suedliche-weinstrasse.saas.smartcjm.com/m/sva/extern/calendar/?uid=527c2cfb-35f9-492c-9676-9d2e7db3ce1d
    - https://stadt-hildesheim.saas.smartcjm.com/m/stadt-hildesheim/extern/calendar/?uid=8b290124-473e-447c-b7a7-6bd74b7c58e5
            
- https://www.rhein-neckar-kreis.de/start/service/terminvereinbarung.html

  Yet another system. Seems to need email and phone before showing dates.

- Yet another system. By *Terminland GmbH*.
    - https://www.terminland.de/Ennepe-Ruhr-Kreis/?m=31789
    - https://www.terminland.eu/impfzentrum_lra-ab/
    - https://www.terminland.de/Lichtenfels/
    
- "Internetgeschaeftsvorfaelle"
    - https://kfz.virtuelles-rathaus.de/igv2-man/servlet/Internetgeschaeftsvorfaelle   
    - https://laikra.komm.one/dvvlaikraIGV21/servlet/Internetgeschaeftsvorfaelle
    
- https://dtms.wiesbaden.de/DTMSTerminWeb/
  
  Yet another system. based on dotnet oO

- https://reservation.frontdesksuite.com/pinneberg/Termin/

- https://termine.crossing.de/319833962/Appointment/Index/1

- Yet another system
    - https://egov.potsdam.de/tnv/?START_OFFICE=kfz
    - https://kfz-termin.landkreis-uelzen.de/?START_OFFICE=KFZZUL
    - https://kfz-termin.landkreis-uelzen.de/?START_OFFICE=KFZAUSGABE

- https://kfzonline.ekom21.de/kfzonline.public/start.html?oe=00.00.06.438000
  
  Don't really finding dates there

- https://www.wormser-baeder.de/sportbaeder/veranstaltungen/eintritt/monatsuebersicht.php

- https://serviceportal.schleswig-holstein.de/Verwaltungsportal/Service/Entry/IKFZ
- https://serviceportal.hamburg.de/HamburgGateway/FVP/FV/Bezirke/DigiTermin/?sid=313


### Started but abandoned 

- https://service.berlin.de/terminvereinbarung/

  Started scraper [berlin.py](src/sources/berlin.py) but they 
  protect themselves with throttling and captchas. They really
  do not want a bot crawling their page. 
 
- [termed.de](https://www.termed.de/) is fully APIfied and there
  exists a prototype of a [scraper](src/sources/termed.py) 
  but it yields such an enormous amount of data 
  (more than 3000 calendars per snapshot leading to gigabytes per week) 
  that it is not included in the data export. Also it's a 
  lot of private medical practices which do not really fit the 
  *public office* category.
  
  To use it, explicitly include it: `python scraper.py snapshot -i termed`
 