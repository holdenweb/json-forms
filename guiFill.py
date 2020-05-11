#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
gui.py: Cut-down interface to be enhanced later. If necessary.

Initially there is no current task, and no duration record.


"""
import logging
import sys

from datetime import datetime

from AnyQt.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QObject,
    QThread,
    Qt,
    QTimer,
)
from AnyQt.QtGui import (
    QFont,
    QIcon,
)
from AnyQt.QtWidgets import (
    QWidget,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QMessageBox,
)

log = logging.getLogger(name="GUI.main")
log.setLevel(logging.INFO)


class TimerThread(QThread):
    """
    Create and connect objects to run in the timer thread's context.

    Note that this __init__ method runs in the context of the _creating_
    thread, and so should not be used to establish signal connections
    for the timer thread. You should do this in the run() method before
    starting the timer thread's event loop.
    """

    def __init__(self, gui):
        log.info("Creating timer thread")
        QThread.__init__(self)
        self.gui = gui
        self.timer = QTimer()
        self.current_task = None
        self.current_duration = None
        self.secs = 0

    def run(self):
        """
        Establish actions that must run in the timer thread.

        At present this is just a single method to run the tests.
        This method runs in the context of the test thread, so
        signals connected here are received by the testing thread.
        """
        log.info("Running timer thread")
        self.timer.timeout.connect(self.tick)
        self.exec_()  # Starts the new thread's event handling loop

    @pyqtSlot()  # Method can be triggered by events
    def tick(self):
        self.secs += 1
        self.gui.time_label.setText(secs_to_hms(self.secs))


def secs_to_hms(secs):
    hrs, secs = divmod(secs, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


class ObjectFiller(QDialog):

    msg_sig = pyqtSignal(str)  # Display this message to the operator
    oyn_sig = pyqtSignal(str)  # Request for operator yes/no

    def __init__(self, form=None, parent=None):
        "Create and display the GUI, but do not start it."
        self.result = None
        self.form  = form
        log.info("Creating GUI object")
        super().__init__(parent=parent)
        self.ui_font = QFont("Microsoft Sans Serif", 12, QFont.Bold)
        self.body_font = QFont("Cooper", 48, QFont.Bold)
        self.setFont(self.ui_font)
        self.app_title = "JSON Forms"
        self.initUI()
        self.tr_thread = TimerThread(self)
        self.tr_thread.start()
        self.show()

    def initUI(self):
        "Create the GUI layout to be used in the tests."
        log.info("Initialising the UI")
        self.setWindowTitle(self.app_title)

        ## Create all necessary widgets
        ## Short aternate names make configuration simpler ;-)
        ## Buttons
        self.submitButton = subb = QPushButton("Submit")
        self.cancelButton = qb = QPushButton("Cancel")
        ## Status bar
        self.time_label = lbl = QLabel("00:00:00", font=self.body_font)

        ## Create the HBoxes containing and laying out the widgets
        ## Status bar
        status_bar = box = QHBoxLayout()
        box.addWidget(lbl)
        ## Buttons
        self.button_bar = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(self.button_bar)
        ## Bring all the HBoxes together in a VBox
        vbox = QVBoxLayout()
        vbox.addLayout(status_bar)
        self.grid = self.form.render()
        vbox.addLayout(self.grid)
        vbox.addWidget(self.button_box)

        ## Connect UI signals to slots
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        ## Establish the window layout
        self.setLayout(vbox)

        ## Set pints.components to desired initial state
        ## tb.setEnabled(False)
        ## sn.setEnabled(False)
        self.setGeometry(300, 300, 300, 250)

    def get_value(self):
        return {f.name: f.widget.text() for f in self.form.fields}

    def show_message(self, msg):
        self.messageArea.setText(msg)

    def add_message(self, msg):
        ma = self.messageArea
        ma.setText(f"{ma.text()}\n\n{msg}")
