from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt
from helpers.config import get_width, get_height
from helpers.weather import get_current_temp_resort, get_current_weather_icon_resort
from helpers.testing_utils import set_random_background_color

class CurrentIcon(QWidget):
    pic_map: QPixmap = None
    icon: QLabel = None

    def __init__(self, parent=None):
        super(CurrentIcon, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.icon = QLabel(self)
        set_random_background_color(self)

    def setIcon(self):
        self.pic_map = QPixmap(
            get_current_weather_icon_resort('killington')
        ).scaled(
            self.width(),
            self.width()
        )
        self.icon.setPixmap(self.pic_map)



class CurrentTemp(QWidget):
    label: QLabel = None
    temp: QLabel = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(CurrentTemp, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("Current Temp")
        self.temp = QLabel(
            str(get_current_temp_resort('killington'))
        )
        self.label.setFixedHeight(int(get_height() * 0.05))
        self.temp.setFixedHeight(int(get_height() * 0.2))
        self.temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.temp, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)
