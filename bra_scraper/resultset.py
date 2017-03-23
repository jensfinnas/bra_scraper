# encoding: utf-8
from bra_scraper.logger import logger
import csvkit as csv

class ResultSet(object):
    """ Represents the response you get from a query
    """
    def __init__(self):
        self._data = Dataset()
        self._notes = Notes()

    @property
    def data(self):
        """ Returns the actual data as a Dataset istance
        """
        return self._data

    @property
    def notes(self):
        """ Returns all notes related to the dataset
        """
        return self._notes

    def add_data(self, data):
        """ Append data
        """
        self._data += data

    def add_note(self, category, note):
        """ Add a note to a category.
            One category can have multiple (but not identical notes)
        
            :param category (str): Name of category
            :param note (Note): The note as a Note instance
        """
        if category not in self._notes:
            self._notes[category] = []

        if note not in self._notes[category]:
            self._notes[category].append(note)

    def note(self, category):
        """ Get a note for a category value (a crime name 
            or region for example)
        """
        try:
            return self._notes[category]
        except:
            raise KeyError(u"There is no note for {}.".format(category))
    


class Dataset(list):
    """ This is where we store the results from the scraper
        Basically a wrapper around Python's native list class.
    """
    def to_csv(self, path):
        logger.info(u"Writing to {}".format(unicode(path,"utf-8")))
        return self.dataframe.to_csv(path, encoding="utf-8")

    @property
    def dataframe(self):
        import pandas as pd
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
                "value": row["value"],
                "status": row["status"],
                })
        return _dictlist
    
    def as_dictlist(self):
        return self

class Notes(dict):
    """ Represents a dict of notes
        Basically a wrapper around Python's native dict class with
        some added export functionality.
    """
    def to_json(self, path):
        """ Save as json
            :param path: file path
        """
        with open(path) as f:
            json.dump(self, f)


    def to_dictlist(self):
        """ Export to list of dicts
        """
        _dictlist = []
        for category, notes in self.iteritems():
            for note in notes:
                #if "\n" in note.note:
                #    import pdb;pdb.set_trace()
                _dictlist.append({
                    "category_id": note.category.id,
                    "category_label": note.category.label,
                    "dimension": note.dimension.name,
                    "note": note.note.replace('\r\n',''),
                    })

        return _dictlist
    

    def to_csv(self, path):
        """ Export to csv based on `.to_dictlist()` representation

            dimension,category,note
            ,,"My general note"
            region,,"My regional note"
            crime,,"My note on crime"
            region,"Stockholms län","My note on Stockholm"
            region,"Stockholms län","My 2nd note on Stockholm"
        """
        logger.info(u"Writing to {}".format(unicode(path,"utf-8")))
        data = self.to_dictlist()
        with open(path, 'wb') as f:
            w = csv.DictWriter(f, data[0].keys())
            w.writeheader()
            w.writerows(data)




