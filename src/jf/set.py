"""
Standard UNIX filtering: JSON input comes from stdin,


Creates empty dictionary if primary key not present.
"""
import json
import shelve
import sys

from hu import DottedDict
from hu import ObjectDict

if __name__ == "__main__":
    import sys

    dbn = "database"
    pk, key = sys.argv[1].split(".", 1)
    with shelve.open(dbn) as db:
        try:
            val = db[pk]
        except KeyError:
            val = {}
        val = DottedDict(val)
        val[key] = json.load(sys.stdin)
        db[pk] = val
