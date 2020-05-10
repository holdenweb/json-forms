"""
qtFields.py - definition of Field objects implemented over AnyQt.
"""
from AnyQt.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QObject,
    QThread,
    Qt,
    QTimer,
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

class Form:

    def __init__(self, fields):
        self.fields = fields

    def render(self):
        """Return a QWidget object that can be added to a layout."""
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        for row, field in enumerate(self.fields):
            grid.addWidget(QLabel(f"{field.title}: ", alignment=Qt.AlignRight), row, 1)
            grid.addWidget(QLineEdit(), row, 2)
        return grid

class Field:

    def __init__(self, name: str, title: str=None, value: str='', input_widget_class=QLineEdit):
        self.name = name
        self.value = value
        self.title = title or value.capitalize()
        self.input_widget_class = input_widget_class


class TextField(Field):

    def render(self):
        """Return a QWidget object that can be added to a Form object using addField."""
        return self.input_widget_class(self.value)

    @property
    def value(self):
        return
