from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt
from helpers.config import get_height


class CurrentIcon(QWidget):
    pic_map: QPixmap = None
    icon: QLabel = None
    icon_path: str = None

    def __init__(self, parent=None, weather_icon_path=''):
        super(CurrentIcon, self).__init__(parent)
        self.icon_path = weather_icon_path
        self.initUI()

    def initUI(self):
        self.icon = QLabel(self)

    def setIcon(self):
        self.pic_map = QPixmap(self.icon_path).scaled(
            self.width(),
            self.width()
        )
        self.icon.setPixmap(self.pic_map)


class CurrentTemp(QWidget):
    label: QLabel = None
    temp: QLabel = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None, cur_temp=''):
        super(CurrentTemp, self).__init__(parent)
        self.initUI(cur_temp=cur_temp)

    def initUI(self, cur_temp):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("Current Temp")
        self.temp = QLabel(cur_temp)
        self.label.setFixedHeight(int(get_height() * 0.05))
        self.temp.setFixedHeight(int(get_height() * 0.2))
        self.temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.temp, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)
