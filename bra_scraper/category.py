# encoding: utf-8

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from copy import deepcopy

class Category(object):
    """ Represents a category in a dimension. Could be a county (if region)
        a crime category or timepoint.
        :param id (int): Four digit id as defined by BRÅ
        :param label (str): Category label
        :level (int): Depth in hiearchy (typically 0-3)
        :parent (Category): Parent category  
    """
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self._label_short = label.split(",")[-1].strip()
        self._parent = None

    @property
    def label_short(self):
        """ Get the last part of a long label.
            Eg. "Hela landet, Stockholms län" => "Stockholms län"
        """
        return self._label_short
    

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def ceased(self):
        """ Has this region/crime ceases to exist?
            returns (bool)
        """
        # TODO: Take into account if the region is relevant
        # in the timepoint for the datapoint.
        return u"upphör" in self.label

    
    def __repr__(self):
        return u"<Category: {}>".format(self.label).encode("utf-8")
                        

MONTHS = ("Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep",
        "Okt","Nov","Dec",)

QUARTER_MONTHS = {
    "Kvartal 1": 1,
    "Kvartal 2": 4,
    "Kvartal 3": 7,
    "Kvartal 4": 10,
}

class Region(Category):
    pass
    

class Period(Category):
    """ Represents a category in the Period dimension
    """

    @property
    def period_start(self):
        """ Get the timepoint of the start of the period.
            :returns (Datetime): 
        """
        period_name = self.label

        if period_name[0:2] == u"År":
            period_name = period_name.replace(u" prel.","")
            year = int(period_name[-4:])

            month = 1
        
        elif u"Helår" in period_name:
            year = int(period_name[:4])
            month = 1
        
        else:
            # "2013, Jun"
            # "2013, Kvartal 2"
            _parts = period_name.split(",")
            year = int(_parts[0][:4])
            _part_of_year = _parts[1].strip()

            try:
                month = QUARTER_MONTHS[_part_of_year]
            except KeyError:
                month = MONTHS.index(_part_of_year) + 1

        return datetime(year=year, month=month, day=1)

    @property
    def period_end(self):
        """ Get the timepoint of the end of the period.
            :returns (Datetime): 
        """
        period_end = deepcopy(self.period_start)
        if self.periodicity == "yearly":
            period_end = period_end + relativedelta(years=1)

        elif self.periodicity == "quarterly":
            period_end = period_end + relativedelta(months=3)

        elif self.periodicity == "monthly":
            period_end = period_end + relativedelta(months=1)

        return period_end - relativedelta(days=1)
        
    
    @property
    def periodicity(self):
        """ :returns (str): Name of periodicity ("yearly", "quarterly", "monthly")
        """
        if (u"Helår" in self.label) or (u"År" in self.label):
            return "yearly"
        elif "Kvartal" in self.label:
            return "quarterly"
        else:
            return "monthly"

    @property
    def preliminary(self):
        """ :returns (bool): Is this a preliminary measure?
        """
        return "Prel" in self.label
    
    def in_range(self, date):
        """ Check if a date is in the range if this period
            :param date (Datetime):
        """
        return (self.period_start <= date) and (date <= self.period_end)

    