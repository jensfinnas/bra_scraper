# encoding: utf-8
import requests
import re
import csvkit as csv
from bra_scraper.surfer import Surfer
from bra_scraper.category import Category, Period, Region


class Dimension(Surfer):
    """ A base class for dimensions in the BRÅ database 
        (Region, Crime, Period)
    """
    def __init__(self, html=None, url=None):
        """ Init with either a html blob or a url from a topic page
            :param html (str): HTML source code from topic page
            :param url (str): Full url of topic page
        """
        super(Dimension, self).__init__()
        if url:
            html = self._fetch_html()
        self._html = html
        # Store all categories in a dict with id as key
        self._categories = self._parse_categories(html) 
        # The id as described in html code, used for parsing categories 
        self._id = None

    @property
    def categories(self):
        return self._categories.values()
    
    def list(self):
        return self.categories

    def get(self, id_or_label):
        """ Get category by id or label
            :returns (Category): 
        """
        try:
            # 1) try id
            return self._categories[id_or_label]
        except KeyError:
            pass

        # 2) try label
        for cat in self.categories:
            if cat.label == id_or_label:
                return cat

        # 3) try end of label
        for cat in self.categories:
            # Labels are long an over explicit, like 
            # "Hela landet, Stockholms län"
            # Hence we check if the end of the label 
            # matches. Eg. "Stockholms län"
            n_chars = len(id_or_label)
            if cat.label[-n_chars:] == id_or_label:
                return cat

        # 4) No match
        else:
            return None

    def to_csv(self, file_path):
        """ Store all categories as a csv file
        """
        columns = ["id", "label", "parent"]
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for category in self.categories:
                if category.parent:
                    parent = category.parent.id
                else:
                    parent = None
                row = [ 
                    category.id,
                    category.label,
                    parent,
                ]
                writer.writerow(row)
 
    def _parse_categories(self, html):
        """ Get categories from HTML code of topic page.
            :param html (str): HTML code of topic page
            :returns: A dict with category id's as keys and
                category instances as values. 
        """
        _categories = {}
        regex_str = r'{}\[\d+\]="(.+)"'.format(self._var_name)
        _categories_raw = re.findall(
            regex_str,
            self._html)

        for _category_string in _categories_raw:
            id, label, parent_id = self._parse_category_string(_category_string)
            _category = self._category_class(id, label)

            if parent_id:
                if parent_id != id:
                    _category.parent = _categories[parent_id]

            _categories[id] = _category

        return _categories


    def _parse_category_string(self, category_string):
        """ Parse id, label and parent of category from strings.
            
            :param category_string (str): For example "8292*Blekinge län*8292*Hela landet, Blekinge län"
            :returns (list): A list with [id, label, parent_id]
        """
         
        _parts = category_string.split("*")
        id = int(_parts[0])

        if len(_parts) == 4:
            label = _parts[3]
        else:
            label = _parts[1].replace("\\xA0","")
        
        if len(_parts) > 2:
            parent_id = int(_parts[2])
        else:
            parent_id = None

        return id, label, parent_id

    def _fetch_html(self):
        """ Get and store the html content of the topic page

            :returns (str): HTML content of the topic page
        """
        self.start_session()
        r = self.session.get(self.url)
        return r.text

class Regions(Dimension):
    """ Represents the regional dimension"""
    def __init__(self, html=None, url=None):
        self.name = "regions"
        # The id used in the html code
        self._var_name = "arrayRegionNiva[Ett|Tva]{3}"
        self._category_class = Region 
        super(Regions, self).__init__(html=html, url=url)


class Crimes(Dimension):
    """ Represents represents the crime"""
    def __init__(self, html=None, url=None):
        self.name = "crimes"
        # The id used in the html code
        self._var_name = "arrayNiva[ett|tva]{3}" # Not the best regex
        self._category_class = Category 

        super(Crimes, self).__init__(html=html, url=url)


class Periods(Dimension):
    """ Represents the time dimension"""
    def __init__(self, html=None, url=None):
        self.name = "periods"
        # The id used in the html code
        self._var_name = "arrayPeriod"
        self._category_class = Period 

        super(Periods, self).__init__(html=html, url=url)

    def _parse_category_string(self, category_string):
        """ Period parsing differs slightly from Region and Crime.
            Hence it gets a different method.
        """
        _parts = category_string.split("*")
        id = int(_parts[0])
        label = _parts[-2]
        parent = None
        return id, label, parent

