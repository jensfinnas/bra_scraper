#!/usr/bin/env python
# coding: utf-8
""" Run the scraper against BRÅ
"""

from modules.interface import Interface
from modules.BRA import BRA

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
        'short': "-o", "long": "--outfile",
        'dest': "outfile",
        'type': str,
        'help': """store result in this file""",
        'required': True,
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
    ui = Interface("Parse Alarm",
                   "Evaluate an alarm, and prepare data for a report",
                   commandline_args=cmd_args)

    scraper = BRA()
    topic_name = unicode(ui.args.topic, "utf-8")
    topic = scraper.topic(topic_name)
    data = topic.query(
        period_start=ui.args.period_start,
        period_end=ui.args.period_end,)
    
    data.to_csv(ui.args.outfile)



if __name__ == '__main__':
    main()
