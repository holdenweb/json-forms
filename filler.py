import sys

from guiFill import mainGUI
from fields import Field


from AnyQt.QtWidgets import QApplication
app = QApplication(sys.argv)
form = [Field(x) for x in  ('first', 'second', 'third')]
gui = mainGUI(form)
app.exec_()
