from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from resources.BaseContainers import BaseHContainer, BaseVContainer
from resources.travel_widgets import TravelInfo, travel_info_stupid_factory
from helpers.config import get_width, get_height
from helpers.testing_utils import set_random_background_color


class ResortInfo(BaseVContainer):
    top_resort_name: QWidget = None
    middle_live_stream: QWidget = None
    bottom_travel_info: TravelInfo = None

    def __init__(self, parent=None, resort='None'):
        super(ResortInfo, self).__init__(parent)
        self.initUI(resort=resort)

    def initUI(self, resort):
        self.top_resort_name = QLabel(resort, parent=self)
        self.middle_live_stream = QWidget(parent=self)
        self.bottom_travel_info = travel_info_stupid_factory(resort, parent=self)
        self.set_sizes()
        self.set_positions()
        for w in (self.middle_live_stream,):
            set_random_background_color(w)

    def set_positions(self):
        self.layout.addWidget(self.top_resort_name, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_live_stream, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_travel_info, alignment=Qt.AlignBottom)

    def set_sizes(self):
        self.top_resort_name.setFixedHeight(int(get_height() * 0.10))
        self.middle_live_stream.setMinimumHeight(int(get_height() * 0.65))
        self.middle_live_stream.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_travel_info.setFixedHeight(int(get_height() * 0.18))
