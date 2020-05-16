"""
qtFields.py - definition of Field objects implemented over AnyQt.
"""
import sys
import datetime

from AnyQt.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, Qt, QTimer
from AnyQt.QtGui import QFont, QIcon
from AnyQt.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QCheckBox,
    QMessageBox,
    QCalendarWidget,
    QFileDialog,
)
from os.path import expanduser
from uuid import uuid4
from guiFill import ObjectFiller


class Form:
    def __init__(self, fields):
        self.fields = fields

    def render(self):
        """Return a QWidget object that can be added to a layout."""
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        for row, field in enumerate(self.fields):
            if not field.hidden:
                grid.addWidget(
                    QLabel(
                        f"{field.title}: ",
                        font=QFont("Microsoft Sans Serif", 24, QFont.Bold),
                        alignment=Qt.AlignRight,
                    ),
                    row,
                    1,
                )
                grid.addWidget(field.render(), row, 2)
        return grid


class Field:
    def __init__(self, name: str, title: str = None, hidden=False, value: str = ""):
        self.name = name
        self.title = title or name.capitalize().replace("_", " ")
        self.hidden = hidden
        self.value = value
        self.widget = None

    def render(self):
        """Return a QWidget object that can be added to a Form object using addField."""
        self.widget = QLineEdit(self.value)
        return self.widget

    def get_value(self):
        """Return whatever the form says should be returned."""
        if self.widget is None:
            return self.value
        else:
            return self.widget.text()


class TimestampField(Field):
    def __init__(self, name, hidden=True, *args, **kwargs):
        super().__init__(name, hidden=hidden, value="**TIMESTAMP**", *args, **kwargs)

    def render(self):
        self.widget = QLabel(self.value)
        return self.widget

    def get_value(self):
        dt = datetime.datetime.now()
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class PlainTextField(Field):
    def render(self):
        self.widget = QPlainTextEdit(self.value)
        return self.widget

    def get_value(self):
        return self.widget.toPlainText()


class TextField(Field):
    pass


class UUIDField(Field):
    def __init__(self, name, title=None, hidden=False, value=None, *args, **kwargs):
        if value is None:
            value = str(uuid4())
        super().__init__(name, title=None, hidden=hidden, value=value, *args, **kwargs)

    def render(self):
        self.widget = QLabel(self.value)
        return self.widget


class DateField(Field):
    def render(self):
        """Return a QWidget object that can be added to a Form object using addField."""
        self.widget = QCalendarWidget()
        return self.widget

    def get_value(self):
        return self.widget.selectedDate().toString(Qt.ISODate)


class ObjectField(Field):
    def __init__(self, name, form=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.form = form

    def render(self):
        self.widget = QPushButton("Edit ...")
        self.widget.clicked.connect(self.get_object)
        return self.widget

    def get_object(self):
        self.gui = ObjectFiller(self.form)
        result = self.gui.exec_()
        # TODO: Should restore values if necessary - QA testing will determine ...

    def get_value(self):
        return {f.name: f.get_value() for f in self.form.fields}


class DirectoryField(ObjectField):
    def render(self):
        self.widget = QPushButton("Select directory ...")
        self.widget.clicked.connect(self.get_object)
        return self.widget

    def get_object(self):
        dialog = QFileDialog()
        self.response = dialog.getExistingDirectory(
            None, "Choose directory", expanduser("~"), QFileDialog.ShowDirsOnly
        )
        if self.response != "":
            self.value = self.response
        return self.response != ""

    def get_value(self):
        """Return whatever the form says should be returned."""
        if self.widget is None:
            return self.value
        else:
            return self.response
