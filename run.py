#!/usr/bin/env python
# coding: utf-8
""" Run the scraper against BRÅ
"""

from bra_scraper.interface import Interface
from bra_scraper.BRA import BRA

def main():
    """ Entry point when run from command line """
    # pylint: disable=C0103

    cmd_args = [{
        'short': "-t", "long": "--topic",
        'dest': "topic",
        'type': str,
        'help': """name of the topic to be scraped (from http://statistik.bra.se/solwebb/action/start?menykatalogid=1)""",
        'default': 'Månads- och kvartalsvis - Kommun och storstädernas stadsdelar 1996-',
    }, {
        'short': "-r", "long": "--regions",
        'dest': "regions",
        'type': str,
        'help': """a comma seprated list of regions to query by""",
    }, {
        'short': "-o", "long": "--outfile",
        'dest': "outfile",
        'type': str,
        'help': """store result in this csv file""",
        'required': True,
    }, {
        'short': "-n", "long": "--notes",
        'dest': "notes",
        'type': str,
        'help': """store notes in this csv file"""
    }, {
        'short': "-ps", "long": "--period_start",
        'dest': "period_start",
        'default': "1900-01-01",
        'type': str,
        'help': """start date (for example 2016-09-01)"""
    }, {
        'short': "-pe", "long": "--period_end",
        'dest': "period_end",
        'default': "2999-01-01",
        'type': str,
        'help': """end date (for example 2016-09-01)"""
    }]
    ui = Interface("Run scraper",
                   "Fetch data from command line",
                   commandline_args=cmd_args)


    # Init
    scraper = BRA(logger=ui)
    topic_name = unicode(ui.args.topic, "utf-8")
    topic = scraper.topic(topic_name)

    # Make query
    if not ui.args.regions:
        regions = "*"
    else:
        regions = ui.args.regions.decode("utf-8").split(",")

    result = topic.query(
        period_start=ui.args.period_start,
        period_end=ui.args.period_end,
        regions=regions,
        )
    
    # Store data
    data_file_path = ui.args.outfile
    result.data.to_csv(data_file_path)
    ui.info(u"Writing to {}".format(unicode(data_file_path,"utf-8")))

    #
    if not ui.args.notes:
        # If note path not defined, write to "mydata_notes.csv" (if "mydata.csv" is data path)
        notes_file = data_file_path.replace(".csv", "_notes.csv")
    else:
        notes_file = ui.args.notes

    if result.notes:
        result.notes.to_csv(notes_file)

if __name__ == '__main__':
    main()
