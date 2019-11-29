from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from helpers.config import get_width, get_height
from helpers.testing_utils import set_random_background_color


class TravelInfo(QWidget):
    left_travel_time: QWidget = None
    right_hotel_info: QWidget = None
    layout: QHBoxLayout = None

    def __init__(self, parent=None):
        super(TravelInfo, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.left_travel_time = QWidget()
        self.right_hotel_info = QWidget()
        self.layout = QHBoxLayout()
        self.set_sizes()
        self.set_positions()
        for w in (self.left_travel_time, self.right_hotel_info):
            set_random_background_color(w)
        self.setLayout(self.layout)

    def set_sizes(self):
        self.left_travel_time.setMinimumWidth(int(get_width() * 0.35))
        self.right_hotel_info.setMinimumWidth(int(get_width() * 0.35))

    def set_positions(self):
        self.layout.addWidget(self.left_travel_time, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right_hotel_info, alignment=Qt.AlignRight)


class ResortInfo(QWidget):
    top_resort_name: QWidget = None
    middle_live_stream: QWidget = None
    bottom_travel_info: TravelInfo = None
    layout: QVBoxLayout = None

    def __init__(self, parent=None):
        super(ResortInfo, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.top_resort_name = QWidget(parent=self)
        self.middle_live_stream = QWidget(parent=self)
        self.bottom_travel_info = TravelInfo(parent=self)
        self.layout = QVBoxLayout()
        self.set_sizes()
        self.set_positions()
        for w in (self.top_resort_name, self.middle_live_stream):
            set_random_background_color(w)
        self.setLayout(self.layout)

    def set_positions(self):
        self.layout.addWidget(self.top_resort_name, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_live_stream, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_travel_info, alignment=Qt.AlignBottom)

    def set_sizes(self):
        self.top_resort_name.setMinimumHeight(int(get_height() * 0.12))
        self.middle_live_stream.setMinimumHeight(int(get_height() * 0.6))
        self.middle_live_stream.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_travel_info.setMinimumHeight(int(get_height() * 0.12))
