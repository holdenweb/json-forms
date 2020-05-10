import sys

from guiFill import mainGUI
from forms import Form, Field


from AnyQt.QtWidgets import QApplication

form_data = [
    {'name': 'first'},
    {'name': 'second'},
    {'name': 'third'},
]
app = QApplication(sys.argv)
form = Form([Field(**x) for x in  form_data])
gui = mainGUI(form)
app.exec_()
