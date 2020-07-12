"""
jlint.py: be kind to readers: render JSON in "canonical form".
"""
import json
import sys

json.dump(json.load(sys.stdin), sys.stdout, indent=2)
print()
