from datetime import datetime
from pprint import pprint

from dateutil import parser
from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel
from PyQt5.QtCore import Qt
from resources.BaseContainers import BaseHContainer, BaseVContainer
from helpers.config import get_width
from helpers.travel import get_travel_info


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
    left_depart_flight: BaseHContainer = None
    middle_return_flight: BaseHContainer = None
    right_flying_price: QWidget = None

    def __init__(self, travel_info=None, parent=None):
        super(TravelInfoFlying, self).__init__(parent)
        self.initUI(travel_info=travel_info.get('info'))

    def initUI(self, travel_info):
        self.left_depart_flight = FlightSegmentsInfo(parent=self, flight_segments_info=travel_info.get('depart'), direction='depart')
        self.middle_return_flight = FlightSegmentsInfo(parent=self, flight_segments_info=travel_info.get('return'), direction='return')
        self.right_flying_price = QLabel(str(travel_info.get('price')))
        self.set_sizes()
        self.set_positions()

    def set_sizes(self):
        self.left_depart_flight.setMinimumWidth(int(get_width() * 0.3))
        self.middle_return_flight.setMinimumWidth(int(get_width() * 0.3))
        self.right_flying_price.setMinimumWidth(int(get_width() * 0.10))

    def set_positions(self):
        self.layout.addWidget(self.left_depart_flight, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle_return_flight, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_flying_price, alignment=Qt.AlignRight)


class FlightSegmentsInfo(BaseVContainer):
    direction: QLabel = None
    flights: BaseHContainer = None

    def __init__(self, parent=None, flight_segments_info=None, direction=None):
        super(FlightSegmentsInfo, self).__init__(parent)
        self.initUI(flight_segments_info=flight_segments_info, direction=direction)

    def initUI(self, flight_segments_info, direction):
        self.direction = QLabel(direction)
        self.flights = FlightSegments(parent=self, flight_segments_info=flight_segments_info)
        self.layout.addWidget(self.direction, alignment=Qt.AlignTop)
        self.layout.addWidget(self.flights, alignment=Qt.AlignBottom, stretch=1)


class FlightSegments(BaseHContainer):
    def __init__(self, parent=None, flight_segments_info=None):
        super(FlightSegments, self).__init__(parent)
        self.initUI(flight_segments_info=flight_segments_info)

    def initUI(self, flight_segments_info):
        if type(flight_segments_info) == str and 'could not find flight info' in flight_segments_info:
            self.layout.addWidget(QLabel(flight_segments_info), alignment=Qt.AlignHCenter)
        else:
            for segment in flight_segments_info:
                self.layout.addWidget(FlightSegment(parent=self, flight_segment_info=segment), alignment=Qt.AlignHCenter)


class FlightSegment(BaseVContainer):
    departAt: datetime = None
    departFrom: str = None
    arriveAt: datetime = None
    arriveIn: str = None

    def __init__(self, parent=None, flight_segment_info=None):
        super(FlightSegment, self).__init__(parent)
        self.departAt = parser.parse(flight_segment_info.get('departAt'))
        self.arriveAt = parser.parse(flight_segment_info.get('arriveAt'))
        self.departFrom = flight_segment_info.get('departFrom')
        self.arriveIn = flight_segment_info.get('arriveIn')
        self.initUI()

    def initUI(self):
        flying_time_string = self.departAt.strftime("%m/%d %H:%M") + " --> " + self.arriveAt.strftime("%m/%d %H:%M")
        self.layout.addWidget(QLabel(self.departFrom + ' --> ' + self.arriveIn), alignment=Qt.AlignTop)
        self.layout.addWidget(QLabel(flying_time_string), alignment=Qt.AlignBottom)
