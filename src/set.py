"""
Standard UNIX filtering: JSON input comes from stdin,


Creates empty dictionary if primary key not present.
"""

import json
import sys
from hu import ObjectDict, DottedDict

import shelve

if __name__ == "__main__":
    import sys

    dbn = "test_db"
    pk, key = sys.argv[1].split(".", 1)
    with shelve.open(dbn, writeback=True) as db:
        try:
            val = db[pk]
        except KeyError:
            val = {}
        val = DottedDict(val)
        val[key] = json.load(sys.stdin)
print()
