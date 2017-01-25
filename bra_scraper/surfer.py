# encoding: utf-8

import requests
from bra_scraper.logger import logger

BASE_URL = "http://statistik.bra.se/"
INTERFACE_URL = BASE_URL + "solwebb/action/"

class Surfer(object):
    """ Common functions for handling sessions etc on the BRÅ site
    """
    def __init__(self):
        self.session = None
        self.BASE_URL = BASE_URL
        self.INTERFACE_URL = INTERFACE_URL

    def start_session(self):
        """ We have to open the pages one by one to get a correct node path
            in our session. Otherwise the site will throw error.
        """
        logger.info("Start new session")
        self.session = requests.session()
        self.session.get(INTERFACE_URL)
        self.session.get(INTERFACE_URL + "/start?menykatalogid=1")