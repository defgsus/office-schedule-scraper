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

Data scraping started at 2021-07-09 for twenty-six cities or districts 
i found through websearch which all use the 
[TEVIS](https://www.kommunix.de/produkte/tevis/) interface.
Other interfaces will be incorporated soon.

I'd like to put the scraped data online like in the
[free parking lots data](https://github.com/defgsus/parking-data/) repository,
but it's going to be a bit more complex, not fitting nicely in CSV tables, i presume.

To scrape yourself:

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
