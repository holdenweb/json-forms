import sys

from guiFill import mainGUI
from forms import Form, Field


from AnyQt.QtWidgets import QApplication
app = QApplication(sys.argv)
form = Form([Field(x) for x in  ('first', 'second', 'third')])
gui = mainGUI(form)
app.exec_()
