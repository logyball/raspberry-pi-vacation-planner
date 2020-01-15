from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from src.resources.base_containers import BaseVContainer
from src.backend.styling import load_stylesheet
from src.backend.config import ConfigFunctions


class SnowReport(BaseVContainer):
    label: QLabel = None
    report: QLabel = None

    def __init__(self, parent: QWidget = None, report: str = None):
        super(SnowReport, self).__init__(parent)
        self.initUI(report=report)
        self._add_stylesheet_info()

    def initUI(self, report: str):
        self.label = QLabel("Today's Weather")
        self.label.setFixedHeight(int(self.config.get_height() * 0.05))
        self.report = QLabel(report)
        self.report.setWordWrap(True)
        self.report.setFixedHeight(int(self.config.get_height() * 0.20))
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

    def __init__(self, parent: QWidget = None, weather_icon_path: str = None):
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


class CurrentTemp(QLabel):
    config: ConfigFunctions = None

    def __init__(self, parent=None, cur_temp=''):
        super(CurrentTemp, self).__init__(parent)
        self.config = ConfigFunctions()
        self.initUI(cur_temp=cur_temp)

    def initUI(self, cur_temp):
        self.setText(cur_temp)
        self.setObjectName('curWeatherTemp')
        self.setFixedHeight(int(self.config.get_height() * 0.22))
        self.setStyleSheet(load_stylesheet('weather_table.qss'))
