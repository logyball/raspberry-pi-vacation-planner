from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QUrl

from src.backend.styling import load_stylesheet
from src.resources.BaseContainers import BaseVContainer
from src.resources.TravelWidgets import TravelInfo, travel_info_stupid_factory
from src.backend.config import get_height, get_stream_path, get_width, get_resort_proper_name


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
    top_resort_name: QLabel = None
    middle_live_stream: CurrentLiveStream = None
    bottom_travel_info: TravelInfo = None

    def __init__(self, parent: QWidget = None, resort: str = None):
        super(ResortInfo, self).__init__(parent)
        self.initUI(resort=resort)

    def initUI(self, resort: str):
        self.top_resort_name = QLabel(get_resort_proper_name(resort))
        self.middle_live_stream = CurrentLiveStream(parent=self, resort=resort)
        self.bottom_travel_info = travel_info_stupid_factory(resort, parent=self)
        self.set_sizes()
        self.set_positions()
        self._set_style()

    def set_positions(self):
        self.layout.addWidget(self.top_resort_name, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_live_stream, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_travel_info, alignment=Qt.AlignBottom)

    def set_sizes(self):
        self.top_resort_name.setFixedHeight(int(get_height() * 0.12))
        self.middle_live_stream.setFixedHeight(int(get_height() * 0.63))
        self.bottom_travel_info.setFixedHeight(int(get_height() * 0.18))

    def _set_style(self):
        self.top_resort_name.setObjectName('resortOfficialTitle')
        self.setStyleSheet(load_stylesheet('resort_info.qss'))
