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
    with shelve.open(db_name) as db:
        val = db[pk]
        yield DottedDict(val)[key]


if __name__ == "__main__":
    import sys

    dbn = "database"
    pk, key = sys.argv[1].split(".", 1)
    with record(dbn, pk, key) as value:
        json.dump(value, sys.stdout)
