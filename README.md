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
| Bauhaus-Universität Weimar Erdgeschoss Raum 002          | etermin    | [www.etermin.net/international-office/](https://www.etermin.net/international-office/)                                                                           |
| BürgerInnenamt Stadt Graz                                | etermin    | [www.etermin.net/buergerinnenamt/](https://www.etermin.net/buergerinnenamt/)                                                                                     |
| Corona TESTZENTRUM im Elithera                           | etermin    | [www.etermin.net/testzentrum1/](https://www.etermin.net/testzentrum1/)                                                                                           |
| Corona Test Braunschweig                                 | etermin    | [www.etermin.net/coronatestbs/](https://www.etermin.net/coronatestbs/)                                                                                           |
| Corona Testcenter                                        | etermin    | [www.etermin.net/ASBTestcenter/](https://www.etermin.net/ASBTestcenter/)                                                                                         |
| Corona-Schnellteststelle Teublitz                        | etermin    | [www.etermin.net/spitzwegapo/](https://www.etermin.net/spitzwegapo/)                                                                                             |
| Corona-Schnelltestzentrum Caspar & Dase für die Wedemark | etermin    | [www.etermin.net/Schnelltestungen/](https://www.etermin.net/Schnelltestungen/)                                                                                   |
| Corona-Testcenter Hersfeld-Rotenburg                     | etermin    | [www.etermin.net/testcenter-hef-rof/](https://www.etermin.net/testcenter-hef-rof/)                                                                               |
| Gemeinde Stahnsdorf                                      | etermin    | [www.etermin.net/stahnsdorf/](https://www.etermin.net/stahnsdorf/)                                                                                               |
| Gesundheitsberuferegister Arbeiterkammer Salzburg        | etermin    | [www.etermin.net/gbr/](https://www.etermin.net/gbr/)                                                                                                             |
| Hochsauerlandkreis                                       | etermin    | [www.etermin.net/hsk-schnelltest/](https://www.etermin.net/hsk-schnelltest/)                                                                                     |
| Ilm-Kreis                                                | tevis      | [tvweb.ilm-kreis.de/ilmkreis/](https://tvweb.ilm-kreis.de/ilmkreis/)                                                                                             |
| Impftermin Thüringen                                     | custom     | [www.impfen-thueringen.de/terminvergabe/](https://www.impfen-thueringen.de/terminvergabe/)                                                                       |
| Jobcenter Bonn                                           | etermin    | [www.etermin.net/jcbn/](https://www.etermin.net/jcbn/)                                                                                                           |
| Kammer für Arbeiter und Angestellte für das Burgenland   | etermin    | [www.etermin.net/GBRBgld/](https://www.etermin.net/GBRBgld/)                                                                                                     |
| Kreis Bergstraße                                         | netappoint | [terminreservierungverkehr.kreis-bergstrasse.de/netappoint/...](https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint/index.php?company=bergstrasse) |
| Kreis Germersheim Kfz-Zulassungsbehörde                  | netappoint | [kfz.kreis-germersheim.de/netappoint/...](https://kfz.kreis-germersheim.de/netappoint/index.php?company=kreis-germersheim)                                       |
| Kreis Groß-Gerau                                         | tevis      | [tevis.ekom21.de/grg/](https://tevis.ekom21.de/grg/)                                                                                                             |
| Kreis Steinfurt                                          | etermin    | [www.etermin.net/kreis-steinfurt/](https://www.etermin.net/kreis-steinfurt/)                                                                                     |
| Kreis Wesel                                              | tevis      | [tevis.krzn.de/tevisweb080/](https://tevis.krzn.de/tevisweb080/)                                                                                                 |
| Landesamt für Mess- und Eichwesen Berlin-Brandenburg     | etermin    | [www.etermin.net/lme-be-bb/](https://www.etermin.net/lme-be-bb/)                                                                                                 |
| Landkreis Bernkastel-Wittlich                            | tevis      | [termine-reservieren.de/termine/bernkastel-wittlich/](https://termine-reservieren.de/termine/bernkastel-wittlich/)                                               |
| Landkreis Cochem-Zell                                    | tevis      | [termine-reservieren.de/termine/cochem-zell/](https://termine-reservieren.de/termine/cochem-zell/)                                                               |
| Landkreis Mayen-Koblenz                                  | tevis      | [termine-reservieren.de/termine/kvmayen-koblenz/](https://termine-reservieren.de/termine/kvmayen-koblenz/)                                                       |
| Landkreis Weilheim-Schongau                              | tevis      | [termine-reservieren.de/termine/weilheimschongau/](https://termine-reservieren.de/termine/weilheimschongau/)                                                     |
| Landratsamt Miesbach                                     | tevis      | [termine-reservieren.de/termine/lra-miesbach/](https://termine-reservieren.de/termine/lra-miesbach/)                                                             |
| Landratsamt München                                      | tevis      | [termine-reservieren.de/termine/lramuenchen/efa/](https://termine-reservieren.de/termine/lramuenchen/efa/)                                                       |
| Magistrat der Stadt Butzbach                             | etermin    | [www.etermin.net/stadtbutzbach/](https://www.etermin.net/stadtbutzbach/)                                                                                         |
| Psychologische Studierendenberatung Innsbruck            | etermin    | [www.etermin.net/PSB-Innsbruck/](https://www.etermin.net/PSB-Innsbruck/)                                                                                         |
| SARS-CoV-2 Testzentrum der Stadt Fürth                   | etermin    | [www.etermin.net/Testzentrum_agnf/](https://www.etermin.net/Testzentrum_agnf/)                                                                                   |
| Schnelltestzentrum Hammersbach                           | etermin    | [www.etermin.net/Schnelltestzentrum/](https://www.etermin.net/Schnelltestzentrum/)                                                                               |
| Stadt Amberg                                             | tevis      | [termine.amberg.de/](https://termine.amberg.de/)                                                                                                                 |
| Stadt Bad-Kreuznach                                      | tevis      | [termine-reservieren.de/termine/svkh/](https://termine-reservieren.de/termine/svkh/)                                                                             |
| Stadt Billerbeck Verwaltung                              | etermin    | [www.etermin.net/termininbillerbeck/](https://www.etermin.net/termininbillerbeck/)                                                                               |
| Stadt Blankenburg (Harz)                                 | etermin    | [www.etermin.net/blankenburg/](https://www.etermin.net/blankenburg/)                                                                                             |
| Stadt Bonn                                               | netappoint | [onlinetermine.bonn.de/...](https://onlinetermine.bonn.de/index.php?company=stadtbonn)                                                                           |
| Stadt Bonn Bauamt                                        | netappoint | [onlinetermine.bonn.de/...](https://onlinetermine.bonn.de/index.php?company=stadtbonn-bau)                                                                       |
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
| Stadt Graz                                               | etermin    | [www.etermin.net/stadtgraz/](https://www.etermin.net/stadtgraz/)                                                                                                 |
| Stadt Gronau                                             | tevis      | [termine-reservieren.de/termine/gronau/](https://termine-reservieren.de/termine/gronau/)                                                                         |
| Stadt Groß-Umstadt                                       | tevis      | [tevis.ekom21.de/gad/](https://tevis.ekom21.de/gad/)                                                                                                             |
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
| Stadt Lehrte                                             | etermin    | [www.etermin.net/StadtLehrte/](https://www.etermin.net/StadtLehrte/)                                                                                             |
| Stadt Leipzig                                            | custom     | [leipzig.de/fachanwendungen/termine/...](https://leipzig.de/fachanwendungen/termine/index.html)                                                                  |
| Stadt Leipzig Standesamt                                 | netappoint | [adressen.leipzig.de/netappoint/...](https://adressen.leipzig.de/netappoint/index.php?company=leipzig-standesamt)                                                |
| Stadt Leun                                               | tevis      | [tevis.ekom21.de/lnx/](https://tevis.ekom21.de/lnx/)                                                                                                             |
| Stadt Linsengericht                                      | tevis      | [tevis.ekom21.de/lsg/](https://tevis.ekom21.de/lsg/)                                                                                                             |
| Stadt Löhne                                              | tevis      | [termine-reservieren.de/termine/loehne/](https://termine-reservieren.de/termine/loehne/)                                                                         |
| Stadt Magdeburg                                          | netappoint | [service.magdeburg.de/netappoint/...](https://service.magdeburg.de/netappoint/index.php?company=magdeburg)                                                       |
| Stadt Mainz                                              | tevis      | [otv.mainz.de/](https://otv.mainz.de/)                                                                                                                           |
| Stadt Minden                                             | tevis      | [termine-reservieren.de/termine/minden/](https://termine-reservieren.de/termine/minden/)                                                                         |
| Stadt Mittenwalde                                        | etermin    | [www.etermin.net/StadtMittenwalde/](https://www.etermin.net/StadtMittenwalde/)                                                                                   |
| Stadt Mörlenbach                                         | tevis      | [tevis.ekom21.de/mah/](https://tevis.ekom21.de/mah/)                                                                                                             |
| Stadt Neu-Isenburg                                       | tevis      | [tevis.ekom21.de/nis/](https://tevis.ekom21.de/nis/)                                                                                                             |
| Stadt Niedenstein                                        | tevis      | [tevis.ekom21.de/nsn/](https://tevis.ekom21.de/nsn/)                                                                                                             |
| Stadt Nordhausen                                         | tevis      | [tevis.svndh.de/](https://tevis.svndh.de/)                                                                                                                       |
| Stadt Ober-Ramstadt                                      | tevis      | [tevis.ekom21.de/oby/](https://tevis.ekom21.de/oby/)                                                                                                             |
| Stadt Oberasbach                                         | etermin    | [www.etermin.net/stadtoberasbach/](https://www.etermin.net/stadtoberasbach/)                                                                                     |
| Stadt Offenbach                                          | tevis      | [tevis.ekom21.de/off/](https://tevis.ekom21.de/off/)                                                                                                             |
| Stadt Paderborn                                          | tevis      | [termine-reservieren.de/termine/paderborn/](https://termine-reservieren.de/termine/paderborn/)                                                                   |
| Stadt Pfungstadt                                         | tevis      | [tevis.ekom21.de/pft/](https://tevis.ekom21.de/pft/)                                                                                                             |
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
| Stadt Weimar                                             | tevis      | [tevis.weimar.de/](https://tevis.weimar.de/)                                                                                                                     |
| Stadt Weiterstadt                                        | tevis      | [tevis.ekom21.de/wdt/](https://tevis.ekom21.de/wdt/)                                                                                                             |
| Stadt Wiehl                                              | etermin    | [www.etermin.net/stadtwiehl/](https://www.etermin.net/stadtwiehl/)                                                                                               |
| Stadt Wittmund                                           | tevis      | [termine-reservieren.de/termine/wittmund/stva/](https://termine-reservieren.de/termine/wittmund/stva/)                                                           |
| Stadt Worms                                              | tevis      | [termine-reservieren.de/termine/worms/](https://termine-reservieren.de/termine/worms/)                                                                           |
| StadtPalais - Museum für Stuttgart                       | etermin    | [www.etermin.net/stadtlaborstuttgart/](https://www.etermin.net/stadtlaborstuttgart/)                                                                             |
| Stadtwerke Geldern Netz                                  | etermin    | [www.etermin.net/Zaehlerwechseltermine/](https://www.etermin.net/Zaehlerwechseltermine/)                                                                         |
| Testzentrum Goslar                                       | etermin    | [www.etermin.net/testzentrumgoslar/](https://www.etermin.net/testzentrumgoslar/)                                                                                 |
| Testzentrum Hahnenklee                                   | etermin    | [www.etermin.net/testzentrumhahnenklee/](https://www.etermin.net/testzentrumhahnenklee/)                                                                         |
| Universität Graz                                         | etermin    | [www.etermin.net/unitestet/](https://www.etermin.net/unitestet/)                                                                                                 |
| Verbandsgemeindeverwaltung Daun                          | etermin    | [www.etermin.net/vgdaun/](https://www.etermin.net/vgdaun/)                                                                                                       |
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

- https://terminonline.neubrandenburg.de/netappoint/index.php?option=showbooking&company=neubrandenburg&cur_cause=1&auth=&month=06&year=2021&sel=8
  
  They seem to have an older (or newer?) version of netappoint belonging to netcallup.de/qmatic

- https://termin.kreis-oh.de/m/kreis-ostholstein/extern/calendar/?uid=e236b01b-460e-4c76-88db-7e083557c438&wsid=c262c86a-9973-4760-806a-bc9c75755014&lang=de

- https://sean.outsystemsenterprise.com/TicketSystemOnlineTermine/

- https://service.berlin.de/terminvereinbarung/

  Started scraper [berlin.py](src/sources/berlin.py) but they 
  protect themselves with throttling and captchas. They really
  do not want a bot crawling their page. 
    
- https://www.radiologie-mannheim.de/online-terminvereinbarung/ is 
  using [termed.de](https://www.termed.de/) which is  
  fully APIfied
  
- https://scheduler.mobimed.at/kinemedic/