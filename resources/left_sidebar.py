from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from helpers.config import get_width, get_height
from helpers.testing_utils import set_random_background_color


class WeatherBar(QWidget):
    left_icon: QWidget = None
    right_temp: QWidget = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(WeatherBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.left_icon = QWidget()
        self.left_icon.setMinimumWidth(int(get_width() * 0.15))
        self.right_temp = QWidget()
        self.right_temp.setMinimumWidth(int(get_width() * 0.15))
        for w in (self.left_icon, self.right_temp):
            set_random_background_color(w)
        self.layout.addWidget(self.left_icon, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_temp, alignment=Qt.AlignHCenter)
        self.setLayout(self.layout)


class LeftSidebar(QWidget):
    top_weather_bar: WeatherBar = None
    middle_snow_report: QWidget = None
    bottom_weather_forecast: QWidget = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(LeftSidebar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.top_weather_bar = WeatherBar(parent=self)
        self.middle_snow_report = QWidget(parent=self)
        self.bottom_weather_forecast = QWidget(parent=self)
        self.top_weather_bar.setMinimumHeight(int(get_height() * 0.25))
        self.middle_snow_report.setMinimumHeight(int(get_height() * 0.30))
        self.middle_snow_report.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_weather_forecast.setMinimumHeight(int(get_height() * 0.4))
        for w in (self.middle_snow_report, self.bottom_weather_forecast):
            set_random_background_color(w)
        self.layout.addWidget(self.top_weather_bar, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_snow_report, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_weather_forecast, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)
