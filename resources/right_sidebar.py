from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QUrl
from resources.BaseContainers import BaseVContainer
from resources.travel_widgets import TravelInfo, travel_info_stupid_factory
from helpers.config import get_height, get_stream_path, get_width


class CurrentLiveStream(QWebEngineView):
    url: QUrl = None

    def __init__(self, parent: QWidget = None, resort: str = None):
        super(CurrentLiveStream, self).__init__(parent)
        self.url = QUrl(get_stream_path(resort_name=resort))
        self.initUI(parent=parent)

    def initUI(self, parent: QWidget):
        self.setFixedWidth(get_width() * 0.7)
        self.setFixedHeight(parent.height())
        self.load(self.url)
        self.triggerPageAction(QWebEnginePage.ReloadAndBypassCache)


class ResortInfo(BaseVContainer):
    top_resort_name: QWidget = None
    middle_live_stream: CurrentLiveStream = None
    bottom_travel_info: TravelInfo = None

    def __init__(self, parent=None, resort='None'):
        super(ResortInfo, self).__init__(parent)
        self.initUI(resort=resort)

    def initUI(self, resort):
        self.top_resort_name = QLabel(resort, parent=self)
        self.middle_live_stream = CurrentLiveStream(parent=self, resort=resort)
        self.bottom_travel_info = travel_info_stupid_factory(resort, parent=self)
        self.set_sizes()
        self.set_positions()

    def set_positions(self):
        self.layout.addWidget(self.top_resort_name, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_live_stream, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_travel_info, alignment=Qt.AlignBottom)

    def set_sizes(self):
        self.top_resort_name.setFixedHeight(int(get_height() * 0.10))
        self.middle_live_stream.setMinimumHeight(int(get_height() * 0.65))
        self.middle_live_stream.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_travel_info.setFixedHeight(int(get_height() * 0.18))
