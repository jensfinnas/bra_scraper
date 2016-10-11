# encoding: utf-8
import re
from datetime import datetime
from math import floor
from lxml import html

from modules.surfer import Surfer
from modules.dimension import Regions, Crimes, Periods
from modules.logger import logger
from modules.utils import parse_value
from modules.dataset import Dataset

import pdb


class Topic(Surfer):
    """ Represents a topic on the BRÅ site
    """
    def __init__(self, label, url, description=None):
        super(Topic, self).__init__()
        self.label = label
        self.menu_id = url.split("=")[-1]
        self.url = self.INTERFACE_URL + "anmalda/urval/urval?menyid=" + self.menu_id
        self.description = description
        self._level = None
        self._html = None
        self._regions = None
        self._crimes = None
        self._periods = None

    @property
    def level(self):
        """ : returns (str): "brottskod" or "brottstyp"
        """
        if not self._level:
            if "brottskod" in self.description:
                self._level = "brottskod"
            elif "brottstyp" in self.description:
                self._level = "brottstyp"
            else:
                msg = u"Could not identify crime level for {}".format(self.label)
                raise ValueError(msg.encode("utf-8"))

        return self._level
    
    @property
    def regions(self):
        if not self._html:
            self._fetch_html()

        if not self._regions:
            self._regions = Regions(html=self._html)

        return self._regions.categories

    @property
    def crimes(self):
        if not self._html:
            self._fetch_html()

        if not self._crimes:
            self._crimes = Crimes(html=self._html)
            
        return self._crimes.categories

    @property
    def periods(self):
        if not self._html:
            self._fetch_html()

        if not self._periods:
            self._periods = Periods(html=self._html)
            
        return self._periods.categories

    

    def query(self, regions="*", crimes="*", period_start="1900-01-01", 
            period_end="2999-1-1", ignore_ceased=True):
        """ Get the data for a set of region, crime and period ids.
            A date range from 2016-03-01 to 2016-04-01 will include
            data for March and Q1 2016, but not April.

            :param regions (list): Region names to be included.
            :param crimes (list): Crime names to be included.
            :param period_start (str|datetime): First timepoint to be included.
            :param period_end (str|datetime): Last timepoint to be included.
            :param ignore_ceased (bool): Skip regions that no longer exist
        """
        if isinstance(period_start, str):
            period_start = datetime.strptime(period_start, "%Y-%m-%d")
        if isinstance(period_end, str):
            period_end = datetime.strptime(period_end, "%Y-%m-%d")
        

        data = []
        queries = []
        region_ids = [x.id for x in self.regions 
            # Filter by regions in query
            if (regions=="*" or x.label in regions) and 
            # Remove ceased
            (not x.ceased or ignore_ceased)
            ]
        crime_ids = [x.id for x in self.crimes 
            if (crimes=="*" or x.label in crimes)]
        period_ids = [x.id for x in self.periods if (x.in_range(period_start) and x.period_end <= period_end)]
        # We can query a maximum of 10 000 datapoints at a time.
        threshold = 10000.0
        n_regions = len(region_ids)
        n_crimes = len(crime_ids)
        n_periods = len(period_ids)
        n_datapoints = n_regions * n_crimes * n_periods

        logger.info(u"Making query of {} regions, {} crimes and {} periods in {}."\
            .format(n_regions, n_crimes, n_periods, self.label))

        logger.info(u"Getting expected {} datapoints"\
            .format(n_datapoints))


        # Group crimes if there are a lot of them
        # TODO: A more generic solution would sort dims by number of categories
        # and optimize the way request queries are put together
        if n_crimes * n_periods > threshold:
            _n = int(floor(threshold / float(n_periods)))
            crime_groups = [ crime_ids[i:i+_n] for i in range(0, n_crimes, _n) ]
        else:
            crime_groups = [ crime_ids ]

        # Make a list of all requests that we will do
        queries = []
        for crime_group in crime_groups:
            n_crimes_in_group = len(crime_group)
            # Group regions to fit within threshold
            _n = int(floor(threshold / float(n_periods) / float(n_crimes_in_group)))
            region_groups = [ region_ids[i:i+_n] for i in range(0, n_regions, _n) ]
            for region_group in region_groups:
                queries.append({
                    "regions": region_group,
                    "crimes": crime_group,
                    "periods": period_ids,
                    })

        # Perform the actual requests
        self.start_session()
        for i, q in enumerate(queries):
            logger.info("Parse result page %s out of %s" % (i+1, len(queries)))
            result_page_html = self._get_result_page(
                q["regions"], q["crimes"], q["periods"])
            data = data + self._parse_result_page(result_page_html)

        """ Start a fresh session. The result page throws an error if 
            we don't open the preceeding selection pages
        """
        """
        self._start_session()
        for i, region_group in enumerate(region_groups):
            logger.info("Parse result page %s out of %s" % (i+1, len(region_groups)))
            result_page = self._get_result_page(region_group, crimes, periods)
            

        """
        logger.info("Parsed %s datapoints" % len(data))

        return Dataset(data)

    def _get_result_page(self,regions, crimes, periods):
        """ Make a query and return the html of the result page.
        """
        payload = {
            "brottstyp_id_string": "*".join([str(x) for x in  crimes]),
            "region_id_string": "*".join([str(x) for x in regions]),
            "period_id_string": "*".join([str(x) for x in periods]),
            "antal_100k":0,
            "antal":1    
        }

        # Make the search
        self.session.get(self.url)
        self.session.post("http://statistik.bra.se/solwebb/action/anmalda/urval/vantapopup", data=payload)
        self.session.get("http://statistik.bra.se/solwebb/action/anmalda/urval/sok")
        r = self.session.get("http://statistik.bra.se/solwebb/action/anmalda/urval/soktabell")

        return r.text

    def _parse_result_page(self, page_content):
        """ Get the datapoints from the result page 
        """
        tree = html.fromstring(page_content)
        data = []

        """ Luckily the value cells all have the same class name 
        """
        for td in tree.xpath("//td[@class='resultatAntal']"):
            ids = td.get("headers").split(" ")
            
            if len(ids) == 1:
                # Empty rows
                continue

            period_id = int(ids[0])
            region_id = int(ids[3])
            crime_id = int(ids[2])
            # TODO: Handle missing more properly
            # Now we just store them as None
            value = parse_value(td.text, "integer")

            datapoint = {
                'period': self._periods.get(period_id),
                'crime': self._crimes.get(crime_id),
                'region': self._regions.get(region_id),
                'value': value,
            }

            data.append(datapoint)

        return data
    
    def _fetch_html(self):
        """ Get and store the html content of the topic page
            :returns (str): HTML content of the topic page
        """
        self.start_session()
        r = self.session.get(self.url)
        self._html = r.text
        return self._html


    def __repr__(self):
        return u"<Topic: {}>".format(self.name).encode("utf-8")