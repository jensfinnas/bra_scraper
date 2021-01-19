# encoding: utf-8

from fixtures import get_topic


def test_query(get_topic):
    topic = get_topic
    res = topic.query(
        regions="Hela landet",
        period_start="2016-01-01",
        period_end="2016-12-31",
        crimes='Brott mot brottsbalken, 3-7 kap. Brott mot person, 6 kap. Sexualbrott',
        measures="*",
    )

    df = res.data.dataframe
    assert df.shape[0] == 2
    for measure in ["count", "per capita"]:
        assert measure in df.measure_id.unique()
