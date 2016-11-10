# encoding: utf-8
import pandas as pd
from modules.logger import logger

class Dataset(list):
    """ This is where we store the results from the scraper
        Basically a wrapper around Python's native list class.
    """
    def to_csv(self, path):
        logger.info(u"Writing to {}".format(unicode(path,"utf-8")))
        return self.dataframe.to_csv(path, encoding="utf-8")

    @property
    def dataframe(self):
        return pd.DataFrame(self.dictlist)
    

    @property
    def dictlist(self):
        _dictlist = []
        for row in self:
            _dictlist.append({
                "period": row["period"].label,
                "period_id": row["period"].id,
                "timepoint": row["period"].period_start,
                "periodicity": row["period"].periodicity,
                "region": row["region"].label,
                "region_id": row["region"].id,
                "crime": row["crime"].label,
                "crime_id": row["crime"].id,
                "value": row["value"]
                })
        return _dictlist
    
    def as_dictlist(self):
        return self