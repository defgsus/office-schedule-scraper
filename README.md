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

|   index | source_id           | scraper    | url                                                                                             |
|--------:|:--------------------|:-----------|:------------------------------------------------------------------------------------------------|
|       1 | bonn                | netappoint | https://onlinetermine.bonn.de/index.php?company=stadtbonn                                       |
|       2 | bonnbau             | netappoint | https://onlinetermine.bonn.de/index.php?company=stadtbonn-bau                                   |
|       3 | dresden             | netappoint | https://termine.dresden.de/netappoint/index.php?company=stadtdresden-fs                         |
|       4 | dresdenkfz          | netappoint | https://termine.dresden.de/netappoint/index.php?company=stadtdresden-kfz                        |
|       5 | egelsbach           | tevis      | https://tevis.ekom21.de/egb                                                                     |
|       6 | frankfurt           | tevis      | https://tevis.ekom21.de/fra                                                                     |
|       7 | friedrichsdorf      | tevis      | https://tevis.ekom21.de/frf                                                                     |
|       8 | grossumstadt        | tevis      | https://tevis.ekom21.de/gad                                                                     |
|       9 | halle               | netappoint | https://ncu.halle.de/index.php?company=stadthalle                                               |
|      10 | heidelberg          | tevis      | https://tevis-online.heidelberg.de                                                              |
|      11 | hornberg            | tevis      | https://tevis.ekom21.de/hbe                                                                     |
|      12 | huenstetten         | tevis      | https://tevis.ekom21.de/hsz                                                                     |
|      13 | huettenberg         | tevis      | https://tevis.ekom21.de/htb                                                                     |
|      14 | ilmkreis            | tevis      | https://tvweb.ilm-kreis.de/ilmkreis                                                             |
|      15 | impfthueringen      | custom     | https://www.impfen-thueringen.de/terminvergabe                                                  |
|      16 | jena                | tevis      | https://tevis-bs.jena.de                                                                        |
|      17 | kaiserslauternausl  | netappoint | https://www3.kaiserslautern.de/netappoint/index.php?company=kaiserslautern-ausl                 |
|      18 | kassel              | tevis      | https://tevis.ekom21.de/kas                                                                     |
|      19 | kelsterbach         | tevis      | https://tevis.ekom21.de/keb                                                                     |
|      20 | kreisbergstrasse    | netappoint | https://terminreservierungverkehr.kreis-bergstrasse.de/netappoint/index.php?company=bergstrasse |
|      21 | kreisgermersheimkfz | netappoint | https://kfz.kreis-germersheim.de/netappoint/index.php?company=kreis-germersheim                 |
|      22 | kreisgrossgerau     | tevis      | https://tevis.ekom21.de/grg                                                                     |
|      23 | kreiswesel          | tevis      | https://tevis.krzn.de/tevisweb080                                                               |
|      24 | leipzigstandesamt   | netappoint | https://adressen.leipzig.de/netappoint/index.php?company=leipzig-standesamt                     |
|      25 | leun                | tevis      | https://tevis.ekom21.de/lnx                                                                     |
|      26 | linsengericht       | tevis      | https://tevis.ekom21.de/lsg                                                                     |
|      27 | magdeburg           | netappoint | https://service.magdeburg.de/netappoint/index.php?company=magdeburg                             |
|      28 | moerlenbach         | tevis      | https://tevis.ekom21.de/mah                                                                     |
|      29 | neuisenburg         | tevis      | https://tevis.ekom21.de/nis                                                                     |
|      30 | niedenstein         | tevis      | https://tevis.ekom21.de/nsn                                                                     |
|      31 | nordhausen          | tevis      | https://tevis.svndh.de                                                                          |
|      32 | oberramstadt        | tevis      | https://tevis.ekom21.de/oby                                                                     |
|      33 | offenbach           | tevis      | https://tevis.ekom21.de/off                                                                     |
|      34 | pfungstadt          | tevis      | https://tevis.ekom21.de/pft                                                                     |
|      35 | viernheim           | tevis      | https://tevis.ekom21.de/vhx                                                                     |
|      36 | weimar              | tevis      | https://tevis.weimar.de                                                                         |
|      37 | weiterstadt         | tevis      | https://tevis.ekom21.de/wdt                                                                     |

The scraped interfaces which are used by most websites:

- **tevis**: https://www.kommunix.de/produkte/tevis/
- **netappoint**: http://www.edv-kahlert.de/produkte/Netcallup/netalarmpro1.htm
  
  (Note that the website url requires a `company` query-parameter to work)


### Data details

At each **snapshot** all **available dates** are recorded for each listed 
office department. The **tevis** system shows the available dates for
the next **N** full weeks, where **N** is set to **8** in my recording job.
The **netappoint** system usually shows the next **28 days** and not more.
 
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

Obviously they offer 5 minute slots. By looking at more data one can see
that *Meldewesen* and *Führerscheinwesen* exchange availability between weeks. 

It's not possible for all websites/systems to gather the actual business
hours for each day so a single snapshot is not necessarily enough to
calculate the correct number of appointments for each day. 

However, when comparing
two successive snapshots, it's possible to count new appointments or 
cancellations quite robustly and then attach a timestamp of when the 
appointments where made, clicked or activated or however this is called.

Still, there seem to be some erratic updates which mess up the calculation
and some offices seem to only update the availability every couple of days. 
From first inspection of the recorded data there is actually not much going on 
at all except for a few cities or districts. Quite sure, this is due to the
pandemic and the *german corps spirit* of bureaucracy in general. 

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

To approximate the number of appointments made per hour,
a snapshot is recorded every minute. Whenever a new snapshot
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
- https://www.leipzig.de/fachanwendungen/termine/index.html

  Using another system (probably) by dmk-ebusiness.de
 