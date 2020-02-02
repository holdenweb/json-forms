"""

Experimental program to mess about with maintaining JSON
data structures as a means of producing usable input data.

Args are:

    1. Database name
    2. Primary key of object

Value fields are provided by data specifications that I
haven't yet really thought about enough.
"""

import json
from hu import ObjectDict, DottedDict

import shelve

from contextlib import contextmanager

@contextmanager
def record(db_name, key):
    with shelve.open(db_name) as db:
        yield DottedDict(db)[key]

if __name__ == "__main__":
    import sys
    dbn = 'test_db'
    key = sys.argv[1]
    with record(dbn, key) as value:
        print(value)
