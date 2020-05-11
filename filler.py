import sys

from guiFill import ObjectFiller
from forms import Form, Field, TextField, TimestampField


from AnyQt.QtWidgets import QApplication

form_data = [
    {'name': 'timestamp', 'type': TimestampField},
    {'name': 'first', 'type': TextField},
    {'name': 'second', 'type': TextField},
    {'name': 'third', 'type': TextField},
]
app = QApplication(sys.argv)
form = Form([x['type'](x['name']) for x in  form_data])
gui = ObjectFiller(form)
app.exec_()
print(gui)
