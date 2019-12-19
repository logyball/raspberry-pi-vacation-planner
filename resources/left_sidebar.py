from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from db.db_logic import WeatherDbReader
from helpers.weather import get_weather_info_from_api
from helpers.config import get_width, get_height, get_db_path
from resources.weather_widgets import CurrentTemp, CurrentIcon
from resources.BaseContainers import BaseVContainer, BaseHContainer
from resources.WeatherForecastTable import WeatherForecastTable


class WeatherBar(BaseHContainer):
    left_icon: CurrentIcon = None
    right_temp: CurrentTemp = None

    def __init__(self, parent=None, todays_weather={}):
        super(WeatherBar, self).__init__(parent)
        self.initUI(todays_weather=todays_weather)

    def initUI(self, todays_weather):
        self.left_icon = CurrentIcon(parent=self, weather_icon_path=todays_weather.get("icon"))
        self.left_icon.setFixedWidth(int(get_width() * 0.15))
        self.left_icon.setIcon()
        self.right_temp = CurrentTemp(parent=self, cur_temp=todays_weather.get("temp"))
        self.right_temp.setFixedWidth(int(get_width() * 0.15))
        self.layout.addWidget(self.left_icon, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_temp, alignment=Qt.AlignHCenter)


class LeftSidebar(BaseVContainer):
    top_weather_bar: WeatherBar = None
    middle_snow_report: QLabel = None
    bottom_weather_forecast: WeatherForecastTable = None
    weather_db_reader: WeatherDbReader = None

    def __init__(self, parent=None, resort=""):
        super(LeftSidebar, self).__init__(parent)
        self.weather_db_reader = WeatherDbReader(get_db_path())
        weather_info = self.weather_db_reader.get_weather_info(resort)
        self.initUI(weather_info=weather_info)

    def initUI(self, weather_info):
        self.top_weather_bar = WeatherBar(parent=self, todays_weather=weather_info.get('today'))
        self.middle_snow_report = QLabel(weather_info.get("today").get("details"))
        self.middle_snow_report.setWordWrap(True)
        self.bottom_weather_forecast = WeatherForecastTable(parent=self, forecast=weather_info.get('forecast'))
        self.top_weather_bar.setFixedHeight(int(get_height() * 0.25))
        self.middle_snow_report.setMaximumHeight(int(get_height() * 0.25))
        self.bottom_weather_forecast.setMinimumHeight(int(get_height() * 0.4))
        self.layout.addWidget(self.top_weather_bar, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_snow_report, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_weather_forecast, alignment=Qt.AlignBottom)
