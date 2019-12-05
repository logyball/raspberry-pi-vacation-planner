from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt
from helpers.weather import get_weather_info
from helpers.config import get_width, get_height
from helpers.testing_utils import set_random_background_color
from resources.weather_widgets import CurrentTemp, CurrentIcon


class WeatherBar(QWidget):
    left_icon: CurrentIcon = None
    right_temp: CurrentTemp = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None, todays_weather={}):
        super(WeatherBar, self).__init__(parent)
        self.initUI(todays_weather=todays_weather)

    def initUI(self, todays_weather):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.left_icon = CurrentIcon(parent=self, weather_icon_path=todays_weather.get("icon"))
        self.left_icon.setFixedWidth(int(get_width() * 0.15))
        self.left_icon.setIcon()
        self.right_temp = CurrentTemp(parent=self, cur_temp=todays_weather.get("temp"))
        self.right_temp.setFixedWidth(int(get_width() * 0.15))
        self.layout.addWidget(self.left_icon, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_temp, alignment=Qt.AlignHCenter)
        self.setLayout(self.layout)


class LeftSidebar(QWidget):
    top_weather_bar: WeatherBar = None
    middle_snow_report: QLabel = None
    bottom_weather_forecast: QWidget = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None, resort="killington"):
        super(LeftSidebar, self).__init__(parent)
        weather_info = get_weather_info(resort)
        self.initUI(weather_info=weather_info)

    def initUI(self, weather_info):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.top_weather_bar = WeatherBar(parent=self, todays_weather=weather_info.get('today'))
        self.middle_snow_report = QLabel(weather_info.get("today").get("details"), parent=self)
        self.middle_snow_report.setWordWrap(True)
        self.bottom_weather_forecast = QWidget(parent=self)
        self.top_weather_bar.setFixedHeight(int(get_height() * 0.25))
        self.middle_snow_report.setMinimumHeight(int(get_height() * 0.30))
        self.middle_snow_report.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_weather_forecast.setMinimumHeight(int(get_height() * 0.4))
        self.layout.addWidget(self.top_weather_bar, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_snow_report, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_weather_forecast, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)
