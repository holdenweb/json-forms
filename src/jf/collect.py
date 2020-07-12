"""
This program, given appropriate specifications, will solicit the
input of a complex data structure element by element, producing
the collected value in JSON form on standard output for further
processing by a JSON pipeline.
"""
import json
import sys

data = {"first": (), "second": (), "third": (), "fourth": ()}

dd = {}
for name, attrs in data.items():
    sys.stderr.write(f"{name}: ")
    dd[name] = input().strip()

json.dump(dd, sys.stdout)
