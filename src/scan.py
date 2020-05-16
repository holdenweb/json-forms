"""
scan.py:    When a new scan appears in the appropriate directory this program is
            triggered with the path of the file as an argument.
"""

from forms import (
    Form,
    Field,
    TextField,
    TimestampField,
    ObjectField,
    DateField,
    PlainTextField,
    DirectoryField,
)
from filler import fill


form = Form(
    [
        TimestampField("scanned_at", hidden=True),
        DateField("document_date"),
        PlainTextField("description"),
        DirectoryField("store_link_at"),
    ]
)
try:
    print(fill(form))
except InterruptedError:
    print("Cancelled by user.")
