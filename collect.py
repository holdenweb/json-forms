import sys
import json

data = (
        ('first', ),
        ('second', ),
        ('third', ),
        ('fourth', ),
    )

dd = {}
for name, in data:
    dd[name] = input(f"{name}: ").strip()

json.dump(dd, sys.stdout)
