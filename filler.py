import sys

from guiFill import mainGUI

from AnyQt.QtWidgets import QApplication
app = QApplication(sys.argv)
gui = mainGUI()
app.exec_()
