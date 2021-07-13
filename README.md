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

- the busyness of the offices over time (e.g. barking at foreigners)
- the desire of citizens to plan ahead (e.g. not taking the first
free slot but one in 4 weeks)
- the most popular time of day for appointments
- the most popular time of day for making appointments
- the cancellation rate 

And all of that for a couple of different cities for comparison. 
As stated earlier: data of enormous importance!

Data scraping started at around 2021-07-09 

I'd like to put the scraped data online like in the
[free parking lots data](https://github.com/defgsus/parking-data/) repository,
but it's going to be a bit more complex, not fitting nicely in CSV tables, i presume.

To collect data yourself:

```shell script
# install
git clone https://github.com/defgsus/office-schedule-scraper
cd office-schedule-scraper
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

# make a snapshot
# where <X> is the number of weeks to look ahead (defaults to 4)
python scraper.py snapshot -w <X>
```

Which leads to a lot of JSON files in the `snapshot` directory. 

Once a couple of other appointment interfaces are implemented i'll think
of a way to unify the scraped data..


### List of implemented websites

Here's a list of websites that are scraped (via `python scraper.py list`):

|   index | source_id           | scraper    | url                                                               |
|--------:|:--------------------|:-----------|:------------------------------------------------------------------|
|       1 | bonn                | netappoint | https://onlinetermine.bonn.de                                     |
|       2 | bonnbau             | netappoint | https://onlinetermine.bonn.de                                     |
|       3 | dresden             | netappoint | https://termine.dresden.de/netappoint                             |
|       4 | dresdenkfz          | netappoint | https://termine.dresden.de/netappoint                             |
|       5 | egelsbach           | tevis      | https://tevis.ekom21.de/egb                                       |
|       6 | frankfurt           | tevis      | https://tevis.ekom21.de/fra                                       |
|       7 | friedrichsdorf      | tevis      | https://tevis.ekom21.de/frf                                       |
|       8 | grossumstadt        | tevis      | https://tevis.ekom21.de/gad                                       |
|       9 | heidelberg          | tevis      | https://tevis-online.heidelberg.de                                |
|      10 | hornberg            | tevis      | https://tevis.ekom21.de/hbe                                       |
|      11 | huenstetten         | tevis      | https://tevis.ekom21.de/hsz                                       |
|      12 | huettenberg         | tevis      | https://tevis.ekom21.de/htb                                       |
|      13 | ilmkreis            | tevis      | https://tvweb.ilm-kreis.de/ilmkreis                               |
|      14 | impfthueringen      | custom     | https://www.impfen-thueringen.de/terminvergabe                    |
|      15 | jena                | tevis      | https://tevis-bs.jena.de                                          |
|      16 | kaiserslauternausl  | netappoint | https://www3.kaiserslautern.de/netappoint                         |
|      17 | kassel              | tevis      | https://tevis.ekom21.de/kas                                       |
|      18 | kelsterbach         | tevis      | https://tevis.ekom21.de/keb                                       |
|      19 | kreisbergstrasse    | netappoint | https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint |
|      20 | kreisgermersheimkfz | netappoint | https://kfz.kreis-germersheim.de/netappoint                       |
|      21 | kreisgrossgerau     | tevis      | https://tevis.ekom21.de/grg                                       |
|      22 | kreiswesel          | tevis      | https://tevis.krzn.de/tevisweb080                                 |
|      23 | leipzigstandesamt   | netappoint | https://adressen.leipzig.de/netappoint                            |
|      24 | leun                | tevis      | https://tevis.ekom21.de/lnx                                       |
|      25 | linsengericht       | tevis      | https://tevis.ekom21.de/lsg                                       |
|      26 | magdeburg           | netappoint | https://service.magdeburg.de/netappoint                           |
|      27 | moerlenbach         | tevis      | https://tevis.ekom21.de/mah                                       |
|      28 | neuisenburg         | tevis      | https://tevis.ekom21.de/nis                                       |
|      29 | niedenstein         | tevis      | https://tevis.ekom21.de/nsn                                       |
|      30 | nordhausen          | tevis      | https://tevis.svndh.de                                            |
|      31 | oberramstadt        | tevis      | https://tevis.ekom21.de/oby                                       |
|      32 | offenbach           | tevis      | https://tevis.ekom21.de/off                                       |
|      33 | pfungstadt          | tevis      | https://tevis.ekom21.de/pft                                       |
|      34 | viernheim           | tevis      | https://tevis.ekom21.de/vhx                                       |
|      35 | weimar              | tevis      | https://tevis.weimar.de                                           |
|      36 | weiterstadt         | tevis      | https://tevis.ekom21.de/wdt                                       |

The scraped interfaces:

- tevis: [https://www.kommunix.de/...](https://www.kommunix.de/produkte/tevis/)
- netappoint: [www.edv-kahlert.de/...](http://www.edv-kahlert.de/produkte/Netcallup/netalarmpro1.htm)


### TODO-list of websites i found

- https://terminonline.neubrandenburg.de/netappoint/index.php?option=showbooking&company=neubrandenburg&cur_cause=1&auth=&month=06&year=2021&sel=8
  
  They seem to have an older (or newer?) version of netappoint belonging to netcallup.de/qmatic

- https://termin.kreis-oh.de/m/kreis-ostholstein/extern/calendar/?uid=e236b01b-460e-4c76-88db-7e083557c438&wsid=c262c86a-9973-4760-806a-bc9c75755014&lang=de
- https://www.leipzig.de/fachanwendungen/termine/index.html

  Using another system (probably) by dmk-ebusiness.de
  
- https://service.magdeburg.de/netappoint/index.php?company=magdeburg
  
  The netappoint configuration is somewhat complex or broken or both. It's
  already hard to get an appoint as a human, let alone as a python script.