"""
Value fields are provided by data specifications that I
haven't yet really thought about enough.
"""

import json
import sys
from hu import ObjectDict, DottedDict

import shelve

from contextlib import contextmanager

@contextmanager
def record(db_name, pk, key):
    with shelve.open(db_name, writeback=True) as db:
        val =  db[pk]
        yield DottedDict(val)


if __name__ == "__main__":
    import sys
    dbn = 'test_db'
    pk = sys.argv[1]
    key = sys.argv[2]
    with record(dbn, pk, key) as value:
         ival = json.load(sys.stdin)
         value[key] = ival

