import sys

from guiFill import ObjectFiller
from forms import Form, Field, TextField, TimestampField, ObjectField


from AnyQt.QtWidgets import QApplication

app = QApplication(sys.argv)

form = Form([
    TimestampField('timestamp'),
    TextField('first'),
    TextField('second'),
    TextField('third'),
    ObjectField('fourth',
                form=Form([TextField('one'),
                           TextField('two')]
                          )
                )
])
gui = ObjectFiller(form, parent=None)
if gui.exec_():
    print(gui.get_value())
else:
    sys.exit("Cancelled by user")
