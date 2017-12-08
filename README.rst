# BRÅ Scraper

This is a Python module for fetching statistical data about reported crime from [Brottsförbyggande rådet](http://statistik.bra.se/solwebb/action/index).

### Installation

`pip install -r requirements.txt`


### Usage

Init scraper:

```python
from bra_scraper.BRA import BRA
scraper = BRA()
```

List topics.

```python
print scraper.topics
```

Explore a topic.

```python

# Get a topic by name (or url)
topic = scraper.topic(u"Månads- och kvartalsvis - Land och län 1975-2014, land och region 2015-")

# Get available regions
print topic.regions

# Get available crimes
print topic.crimes

```

Make query.

```python
# Query date range
data = topic.query(period_start="2016-01-01", period_end="2016-06-30")

# Query by region and crimes
data = topic.query(regions=["Bjuv kommun"], crimes=[u"Våldsbrott"])

# Query by measure
data = topic.query(regions=["Hela riket"], measures=["count", "per capita"])
```

Save results.

```python
data.to_csv("my_data_dump.csv")
```

### Command line usage

With `run.py` you can run the scraper from the command line. Run `python run.py --help` for help:

```
  -t TOPIC, --topic TOPIC
                        name of the topic to be scraped (from http://statistik
                        .bra.se/solwebb/action/start?menykatalogid=1)
  -o OUTFILE, --outfile OUTFILE
                        store result in this file
  -ps PERIOD_START, --period_start PERIOD_START
                        start date (for example 2016-09-01)
  -pe PERIOD_END, --period_end PERIOD_END
                        end date (for example 2016-09-01)
```
