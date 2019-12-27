from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from random import randint
colors = [Qt.white, Qt.black, Qt.blue, Qt.red, Qt.green, Qt.gray, Qt.darkYellow, Qt.darkBlue, Qt.lightGray, Qt.darkMagenta, Qt.darkGreen]


def set_random_background_color(widget: QWidget):
    pal = widget.palette()
    pal.setColor(QPalette.Window, colors[randint(0, len(colors) - 1)])
    widget.setAutoFillBackground(True)
    widget.setPalette(pal)
