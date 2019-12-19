from PyQt5.QtWidgets import QLabel, QWidget, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from helpers.config import get_width, get_height
from resources.BaseContainers import BaseVContainer, BaseHContainer
from helpers.styling import load_stylesheet


class TableIcon(QWidget):
    pic_map: QPixmap = None
    icon: QLabel = None
    icon_path: str = None

    def __init__(self, parent=None, weather_icon_path=''):
        super(TableIcon, self).__init__(parent)
        self.icon_path = weather_icon_path
        self.initUI()

    def initUI(self):
        self.icon = QLabel(self)

    def setIcon(self):
        self.pic_map = QPixmap(self.icon_path).scaled(
            self.height(),
            self.height()
        )
        self.icon.setPixmap(self.pic_map)


class WeatherTableRow(BaseHContainer):
    date: QLabel = None
    icon: TableIcon = None
    forecast: QLabel = None

    def __init__(self, parent=None, dayInfo: dict = None):
        super(WeatherTableRow, self).__init__(parent)
        self.initUI(dayInfo)
        self._set_style()

    def initUI(self, dayInfo: dict):
        self.date = QLabel(dayInfo.get("date"))
        self.date.setFixedWidth(int(get_width() * 0.05))
        self.icon = TableIcon(parent=self, weather_icon_path=dayInfo.get("icon"))
        self.icon.setFixedWidth(int(get_width() * 0.03))
        self.icon.setIcon()
        self.forecast = QLabel(dayInfo.get("forecast"))
        self.forecast.setFixedWidth(int(get_width() * 0.2))
        self.forecast.setWordWrap(True)
        self.layout.addWidget(self.date, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.forecast, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.icon, alignment=Qt.AlignHCenter)
        self.setFrameShape(QFrame.Panel)

    def _set_style(self):
        self.date.setObjectName('weatherRowDate')
        self.forecast.setObjectName('weatherRowForecast')
        self.setStyleSheet(load_stylesheet('weather_table.qss'))


class WeatherForecastTable(BaseVContainer):
    header: QLabel = None
    rows: list = None

    def __init__(self, parent=None, forecast=None):
        super(WeatherForecastTable, self).__init__(parent)
        self.initUI(forecast=forecast)
        self._build_table(forecast=forecast)
        self._set_style()

    def initUI(self, forecast):
        self.rows = []
        amount_of_days = len(forecast)
        self.header = QLabel(str(amount_of_days) + " DAY FORECAST:")
        self.header.setFixedHeight(int(get_height() * 0.03))
        self.layout.addWidget(self.header, alignment=Qt.AlignTop)

    def _build_table(self, forecast):
        for day in forecast:
            self.rows.append(
                WeatherTableRow(parent=self, dayInfo=day)
            )
        for row in self.rows:
            self.layout.addWidget(row, alignment=Qt.AlignTop)
            row.setFixedHeight(int(get_height() * 0.065))

    def _set_style(self):
        self.header.setObjectName('weatherTableHeader')
        self.setStyleSheet(load_stylesheet('weather_table.qss'))
