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
        self.exec_()

    @pyqtSlot()  # Method can be triggered by events
    def tick(self):
        self.secs += 1
        self.gui.time_label.setText(secs_to_hms(self.secs))


def secs_to_hms(secs):
    hrs, secs = divmod(secs, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


class mainGUI(QWidget):

    msg_sig = pyqtSignal(str)  # Display this message to the operator
    oyn_sig = pyqtSignal(str)  # Request for operator yes/no

    def __init__(self, form):
        "Create and display the GUI, but do not start it."
        self.form  = form
        log.info("Creating GUI object")
        QWidget.__init__(self)
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
        self.quitButton = qb = QPushButton("Quit")
        ## Status bar
        self.time_label = lbl = QLabel("00:00:00", font=self.body_font)

        ## Create the HBoxes containing and laying out the widgets
        ## Status bar
        status_bar = box = QHBoxLayout()
        box.addWidget(lbl)
        ## Buttons
        button_bar = box = QHBoxLayout()
        box.addWidget(qb)
        box.addWidget(subb)
        ## Bring all the HBoxes together in a VBox
        vbox = QVBoxLayout()
        vbox.addLayout(status_bar)
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        for row, field in enumerate(self.form):
            grid.addWidget(QLabel(field.name, alignment=Qt.AlignRight), row, 1)
            grid.addWidget(QLineEdit("Value?"), row, 2)
        vbox.addLayout(grid)

        vbox.addLayout(button_bar)

        ## Connect UI signals to slots
        #cs.currentIndexChanged.connect(self.new_customer_selected)
        #ps.currentIndexChanged.connect(self.new_project_selected)
        #ts.currentIndexChanged.connect(self.new_task_selected)
        self.quitButton.clicked.connect(self.close)

        ## Establish the window layout
        self.setLayout(vbox)

        ## Set pints.components to desired initial state
        ## tb.setEnabled(False)
        ## sn.setEnabled(False)
        self.setGeometry(300, 300, 300, 250)

    @pyqtSlot(int)
    def new_customer_selected(self, i):
        "Handle change of customer by switching projects."
        key = self.project_selector.selected_key
        log.info(f"Project selected: {i}, key {key}")
        self.customer_selector.populate_chained()

    @pyqtSlot(int)
    def new_project_selected(self, i):
        "Handle change of project by switching tasks."
        key = self.project_selector.selected_key
        log.info(f"Project selected: {i}, key {key}")
        self.project_selector.populate_chained()

    @pyqtSlot(int)
    def new_task_selected(self, i):
        self.pauseButton.clicked.emit()
        key = self.task_selector.selected_key
        log.info(f"Task selected: {i}, key {key}")
        if key not in self.task_windows:
            self.task_windows[key] = taskGUI(key)
        new_window = self.task_windows[key]
        new_window.show()
        new_window.raise_()

    def show_message(self, msg):
        self.messageArea.setText(msg)

    def add_message(self, msg):
        ma = self.messageArea
        ma.setText(f"{ma.text()}\n\n{msg}")

    # @pyqtSlot(str)
    # def operator_yes_no(self, msg):
    # answer = QMessageBox.question(
    # None,
    # "Confirm Test Sucess",
    # msg,
    # QMessageBox.Yes | QMessageBox.No,
    # QMessageBox.No,
    # )
    ## Signal the caller that the result was received.
    # self.ryn_sig.emit(answer == QMessageBox.Yes)


class taskGUI(QWidget):
    def __init__(self, task_id):
        QWidget.__init__(self)
        self.task = session.query(Task).filter(Task.id == task_id).one()
        self.initUI()

    def initUI(self):

        self.body_font = QFont("Cooper", 48, QFont.Bold)
        self.time_label = tlbl = QLabel("00:00:00", font=self.body_font)
        self.proj_label = QLabel(self.task.project.description)
        self.task_label = QLabel(self.task.description)
        self.startButton = stab = QPushButton("Start")
        self.pauseButton = pb = QPushButton("Pause")
        self.finishButton = fb = QPushButton("Finish")

        self.project_bar = box = QHBoxLayout()
        box.addWidget(QLabel("Project:"))
        box.addStretch(1)
        box.addWidget(self.proj_label)

        self.task_bar = box = QHBoxLayout()
        box.addWidget(QLabel("Task:"))
        box.addStretch(1)
        box.addWidget(self.task_label)

        self.button_box = box = QVBoxLayout()
        box.addWidget(stab)
        box.addStretch(1)
        box.addWidget(pb)
        box.addStretch(1)
        box.addWidget(fb)

        self.time_bar = box = QHBoxLayout()
        box.addWidget(tlbl)
        box.addStretch(1)
        box.addLayout(self.button_box)

        # Bring all the HBoxes together in a VBox
        vbox = QVBoxLayout()
        vbox.addLayout(self.project_bar)
        vbox.addLayout(self.task_bar)
        vbox.addLayout(self.time_bar)

        self.setLayout(vbox)
