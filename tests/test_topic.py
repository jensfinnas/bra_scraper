# encoding: utf-8

from fixtures import get_topic
from bra_scraper.dimension import Crimes, Regions, Periods

def test_dimension_from_category(get_topic):
    """ Assert that ._dimension_from_category() works
    """
    topic = get_topic
    dim_by_label = topic._dimension_from_category(u"Hela landet, Västra Götalands län")
    dim_by_short_label = topic._dimension_from_category(u"Västra Götalands län")
    dim_by_missing_label = topic._dimension_from_category(u"foo")

    assert isinstance(dim_by_label, Regions)
    assert isinstance(dim_by_short_label, Regions)
    assert dim_by_missing_label == None
