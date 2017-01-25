# encoding: utf-8
import requests
from lxml import html
from bra_scraper.topic import Topic
from bra_scraper.surfer import Surfer


class BRA(Surfer):
    """ The entry point for site scraping
    """
    def __init__(self):
        super(BRA, self).__init__()
        self._topics = None

    @property
    def topics(self):
        """ Get a list of all topic
            :returns (list): A list of Topic instances 
        """
        if not self._topics:
            _topics = []
            r = requests.get(self.BASE_URL + "solwebb/action/start?menykatalogid=1")
            _html = r.content
            _tree = html.fromstring(_html)
            links = _tree.xpath("//li[@class='menySol']/a")
            
            for link in links:
                url = link.get("href")
                name = link.xpath("span[@class='menytext']")[0].text
                desc = link.xpath("../following-sibling::li[@class='menyText']")[0].text
                _topic = Topic(name, url, desc)
                _topics.append(_topic)

            self._topics = _topics

        return self._topics

    def topic(self, label_or_url, level="brottstyp"):
        """ Get topic by label or url
            :param label_or_url: Label (e.g "Årsvis - Kommun och storstädernas stadsdelar 1996-")
                or url (e.g "http://statistik.bra.se/solwebb/action/anmalda/urval/urval?menyid=101")
            :param level: "brottskod" | "brottstyp"     
            :returns (Topic):
        """
        try:
            if "http" in label_or_url:
                # Get by url
                return [x for x in self.topics if x.url == label_or_url ][0]
            else:
                # Get by label
                return [x for x in self.topics if x.label == label_or_url and x.level == level][0]
        except IndexError:
            return None
    
