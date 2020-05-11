import sys

from guiFill import ObjectFiller
from forms import Form, Field, TextField, TimestampField


from AnyQt.QtWidgets import QApplication, QMainWindow

form_data = [
    {'name': 'timestamp', 'type': TimestampField},
    {'name': 'first', 'type': TextField},
    {'name': 'second', 'type': TextField},
    {'name': 'third', 'type': TextField},
]
app = QApplication(sys.argv)
form = Form([x['type'](x['name']) for x in  form_data])
main_window = QMainWindow()
gui = ObjectFiller(form, parent=main_window)
app.exec_()
print(gui.get_value())
