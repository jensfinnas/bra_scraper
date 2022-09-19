# encoding: utf-8

import requests

BASE_URL = "https://statistik.bra.se/"
INTERFACE_URL = BASE_URL + "solwebb/action/"

class Surfer(object):
    """ Common functions for handling sessions etc on the BRÅ site
    """
    def __init__(self, logger=None):
        """ :param: 
        """
        self.session = None
        self.BASE_URL = BASE_URL
        self.INTERFACE_URL = INTERFACE_URL
        if logger is None:
            logger = SilentLogger()
        self.logger = logger

    def start_session(self):
        """ We have to open the pages one by one to get a correct node path
            in our session. Otherwise the site will throw error.
        """
        self.log.info("Start new session")
        self.session = requests.session()
        self.session.get(INTERFACE_URL)
        self.session.get(INTERFACE_URL + "/start?menykatalogid=1")

    @property
    def log(self):
        return self.logger

class SilentLogger():
    """ Empyt "fake" logger
    """

    def log(self, msg, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass
