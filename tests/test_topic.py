# encoding: utf-8

from fixtures import get_topic
from bra_scraper.dimension import Crimes, Regions, Periods

def _test_get_regions(get_topic):
    topic = get_topic
    regions = topic.dimension("regions").categories
    assert len(regions) > 0
    assert regions[0] is not None


def test_measure_dimension(get_topic):
    topic = get_topic
    assert len(topic.dimension("measures").categories) == 2

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
