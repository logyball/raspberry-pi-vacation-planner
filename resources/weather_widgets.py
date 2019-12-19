from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from resources.BaseContainers import BaseVContainer
from helpers.config import get_height, get_resort_proper_name
from helpers.styling import load_stylesheet


class SnowReport(BaseVContainer):
    label: QLabel = None
    report: QLabel = None

    def __init__(self, parent: QWidget = None, report: str = None, resort: str = None):
        super(SnowReport, self).__init__(parent)
        self.initUI(report=report, resort=resort)
        self._add_stylesheet_info()

    def initUI(self, report: str, resort: str):
        self.label = QLabel(f"Today's Weather for {get_resort_proper_name(resort)}: ")
        self.label.setFixedHeight(int(get_height() * 0.05))
        self.report = QLabel(report)
        self.report.setWordWrap(True)
        self.report.setFixedHeight(int(get_height() * 0.5))
        self.layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.report, alignment=Qt.AlignBottom)

    def _add_stylesheet_info(self):
        self.label.setObjectName('todayWeatherReportLabel')
        self.report.setObjectName('todayWeatherReportText')
        self.setStyleSheet(load_stylesheet('weather_table.qss'))


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


class CurrentTemp(BaseVContainer):
    label: QLabel = None
    temp: QLabel = None

    def __init__(self, parent=None, cur_temp=''):
        super(CurrentTemp, self).__init__(parent)
        self.initUI(cur_temp=cur_temp)

    def initUI(self, cur_temp):
        self.label = QLabel()
        self.temp = QLabel(cur_temp)
        self.temp.setObjectName('curWeatherTemp')
        self.label.setObjectName('curWeatherLabel')
        self.label.setFixedHeight(int(get_height() * 0.05))
        self.temp.setFixedHeight(int(get_height() * 0.2))
        self.layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.temp, alignment=Qt.AlignBottom)
        self.setStyleSheet(load_stylesheet('weather_table.qss'))
