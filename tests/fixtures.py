# encoding: utf-8

import pytest
from bra_scraper import BRA


@pytest.fixture(scope="session")
def get_topic():
    """ Set up scraper and return a topic instance
    """
    bra = BRA()
    topic = bra.topic(u"Årsvis - Land och län 1975-2014, land och region 2015-")
    return topic