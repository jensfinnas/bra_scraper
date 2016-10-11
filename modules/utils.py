# encoding: utf-8
from datetime import datetime

def parse_float(value):
    return float(value)

def parse_int(value):
    return int(float(value))

def parse_value(value, value_type, date_format="%Y-%m-%d"):
    _value = None

    if value_type == "float":
        try:
            _value = parse_float(value.replace(",", "."))
        except (TypeError, AttributeError):
            _value = None
    
    elif value_type == "integer":
        try:
            _value = parse_int(value.replace(" ", "").replace(u"\xa0",""))
        except ValueError:
            _value = None

    elif value_type == "datetime":
        _value = datetime.strptime(value, date_format)

    elif isinstance(value, basestring):
        _value = value

    return _value



def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]



from itertools import product
from collections import defaultdict


""" GROUP QUERIES
""" 

def srange(start, stop, step):
    """ Like range(), but with custom incrementation
    """
    r = start
    while r < stop:
        yield r
        r += step

def get_basepoint(ll, chunk_size):
    """ Get the index of the basepoint, that is the last
        datapoint that fits in a single query 
    """
    prev = 1
    for i, l in enumerate(ll):
        if prev * len(l) > chunk_size:
            j = int(float(chunk_size) / float(prev))
            return (i, j)
        prev = prev * len(l)
    return (len(ll), 0)


def make_increments(i, j, ll):
    step = max(j,1)
    return [(x, min(x + step, len(ll[i]))) for x in srange(j, len(ll[i]), step)]

def group_queries(ll, chunk_size):
    """ Pass a list of lists and compose a list of query combinations
        that, when multiplied, do not exceed a given chunk size. 
    """
    #print "*** group (chunk_size: %s) ***" % chunk_size
    
    # Sort lists by length, but also store original order so that we can return
    # the original sorting
    list_lengths = [len(l) for l in ll]
    list_lengths, original_order, ll = zip(*sorted(zip(list_lengths, range(0,len(ll)), ll)))

    # The "basepoint" is the last datapoint that fits in a single query 
    bp = get_basepoint(ll, chunk_size)
    i,j = bp[0],bp[1]
    indecies = defaultdict(list)
    
    # Base query
    for _i in range(0,i):
        indecies[_i].append((0,len(ll[_i])))
    if i < len(ll):
        indecies[i] = [(0,j)] + make_increments(i, j, ll) 

    # Query ranges that are added "on top" of the base query
    for _i in range(i+1,len(ll)):
        indecies[_i] = make_increments(_i, 0, ll) 

    queries_i = list(product(*indecies.values()))
    queries = []
    for i, q in enumerate(queries_i):
        # Populate the queries with actual values (instead of indecies)
        values = [ ll[i][x[0]:x[1]] for i, x in enumerate(q)]
        
        # Get the size of the current query
        # size = reduce(lambda x,y: x*y, [len(l) for l in values])

        # Revert to original sorting
        sorted_order, values = zip(*sorted(zip(original_order, values)))
        queries.append(values)

    return queries