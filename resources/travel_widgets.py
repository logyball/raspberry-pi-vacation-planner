from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from resources.BaseContainers import BaseHContainer, BaseVContainer
from helpers.config import get_width
from helpers.travel import get_travel_info
from helpers.testing_utils import set_random_background_color


def travel_info_stupid_factory(resort, parent=None):
    travel_info = get_travel_info(resort=resort)
    if travel_info.get("mode", "flying") == "flying":
        return TravelInfoFlying(travel_info=travel_info, parent=parent)
    return TravelInfoDriving(travel_info=travel_info, parent=parent)


class TravelInfo(BaseHContainer):
    def __init__(self, parent=None):
        super(TravelInfo, self).__init__(parent)


class TravelInfoDriving(TravelInfo):
    left_drive_time: QWidget = None
    # middle_driving_directions: QWidget = None
    right_driving_distance: QWidget = None

    def __init__(self, travel_info=None, parent=None):
        super(TravelInfoDriving, self).__init__(parent)
        self.initUI(travel_info=travel_info.get('info'))

    def initUI(self, travel_info):
        self.left_drive_time = QLabel("Driving time: " + travel_info.get('time'))
        self.right_driving_distance = QLabel("Driving distance: " + travel_info.get('distance'))
        for w in (self.left_drive_time, self.right_driving_distance):
            w.setWordWrap(True)
        self.set_sizes()
        self.set_positions()

    def set_sizes(self):
        self.left_drive_time.setMinimumWidth(int(get_width() * 0.35))
        self.right_driving_distance.setMinimumWidth(int(get_width() * 0.35))

    def set_positions(self):
        self.layout.addWidget(self.left_drive_time, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right_driving_distance, alignment=Qt.AlignRight)


class TravelInfoFlying(TravelInfo):
    left_flight_info: QWidget = None
    middle_flight_time: QWidget = None
    right_flying_price: QWidget = None

    def __init__(self, travel_info=None, parent=None):
        super(TravelInfoFlying, self).__init__(parent)
        self.initUI(travel_info=travel_info.get('info'))

    def initUI(self, travel_info):
        self.left_flight_info = QLabel(travel_info.get('depart'))
        self.middle_flight_time = QLabel(travel_info.get('return'))
        self.right_flying_price = QLabel(travel_info.get('price'))
        for w in (self.left_flight_info, self.middle_flight_time, self.right_flying_price):
            w.setWordWrap(True)
        self.set_sizes()
        self.set_positions()

    def set_sizes(self):
        self.left_flight_info.setMinimumWidth(int(get_width() * 0.35))
        self.middle_flight_time.setMinimumWidth(int(get_width() * 0.15))
        self.right_flying_price.setMinimumWidth(int(get_width() * 0.2))

    def set_positions(self):
        self.layout.addWidget(self.left_flight_info, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle_flight_time, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_flying_price, alignment=Qt.AlignRight)
