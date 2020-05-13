"""
qtFields.py - definition of Field objects implemented over AnyQt.
"""
import sys
from datetime import datetime

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
    QCheckBox,
    QMessageBox,
)

from guiFill import ObjectFiller


class Form:
    def __init__(self, fields):
        self.fields = fields

    def render(self):
        """Return a QWidget object that can be added to a layout."""
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        for row, field in enumerate(self.fields):
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
    def __init__(self, name: str, title: str = None, value: str = ""):
        self.name = name
        self.title = title or name.capitalize()
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
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, value="**TIMESTAMP**", *args, **kwargs)

    def render(self):
        return QLabel(self.value)

    def get_value(self):
        dt = datetime.now()
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class TextField(Field):
    pass


class ObjectField(Field):
    def __init__(self, name, form, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.form = form

    def render(self):
        self.widget = QPushButton(f"{self.name} ...")
        self.widget.clicked.connect(self.get_object)
        return self.widget

    def get_object(self):
        self.gui = ObjectFiller(self.form)
        result = self.gui.exec_()
        # TODO: Should restore values if necessary - QA testing will determine ...

    def get_value(self):
        return {f.name: f.get_value() for f in self.form.fields}
