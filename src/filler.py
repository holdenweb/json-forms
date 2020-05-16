import json
import sys

from guiFill import ObjectFiller
from forms import (
    Form,
    Field,
    TextField,
    TimestampField,
    ObjectField,
    DateField,
    UUIDField,
    PlainTextField,
)


from AnyQt.QtWidgets import QApplication

app = QApplication(sys.argv)

form = Form(
    [
        TimestampField("scan_time", hidden=True),
        UUIDField("identity"),
        DateField("dated"),
        PlainTextField("description"),
        TextField("tags"),
        ObjectField("fourth", form=Form([TextField("one"), TextField("two")])),
    ]
)


def fill(form):
    gui = ObjectFiller(form, parent=None)
    if gui.exec_():
        return gui.get_value()
    else:
        raise InterruptedError()


if __name__ == "__main__":
    try:
        json.dump(fill(form), sys.stdout)
        print()
    except InterruptedError:
        sys.exit("Cancelled by user")
