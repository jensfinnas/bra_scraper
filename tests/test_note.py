# encoding: utf-8

import pytest
from fixtures import get_topic
from bra_scraper.note import Note

def test_creating_basic_note(get_topic):
    """ Assert that ._dimension_from_category() works
    """
    topic = get_topic
    dim = topic.dimension("regions")
    good_note = Note("My note", u"Stockholms län", dim)
    assert good_note.note == "My note"

def test_creating_note_on_wrong_category(get_topic):
    """ Assert that a note placed on a non exsiting category
        raises error.
    """
    topic = get_topic
    dim = topic.dimension("regions")
    with pytest.raises(Exception):
        Note("My note", u"non existing region", dim)
