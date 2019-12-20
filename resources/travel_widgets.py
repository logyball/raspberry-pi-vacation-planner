from datetime import datetime
from dateutil import parser
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from db.db_logic import TravelDbReader
from helpers.styling import load_stylesheet
from resources.BaseContainers import BaseHContainer, BaseVContainer
from helpers.config import get_width, get_db_path, get_height


def travel_info_stupid_factory(resort, parent=None):
    db_reader = TravelDbReader(get_db_path())
    travel_info = db_reader.get_travel_info(resort=resort)
    if travel_info.get("mode", "flying") == "flying":
        return TravelInfoFlying(travel_info=travel_info, parent=parent)
    return TravelInfoDriving(travel_info=travel_info, parent=parent)


class TravelInfo(BaseHContainer):
    def __init__(self, parent=None):
        super(TravelInfo, self).__init__(parent)


class DriveDistance(BaseVContainer):
    label: QLabel = None
    distance: QLabel = None

    def __init__(self, parent: QWidget = None, distance: str = None):
        super(DriveDistance, self).__init__(parent)
        self.label = QLabel('Driving Distance')
        self.time = QLabel(distance)
        self._set_style()

    def _set_style(self):
        self.label.setObjectName('driveDistanceLabel')
        self.time.setObjectName('driveDistanceValue')
        self.time.setFixedHeight(int(get_height() * 0.15))
        self.layout.addWidget(self.time, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.label, alignment=Qt.AlignBottom)
        self.setStyleSheet(load_stylesheet('travel_styles.qss'))


class DriveTime(BaseVContainer):
    label: QLabel = None
    time: QLabel = None

    def __init__(self, parent: QWidget = None, time: str = None):
        super(DriveTime, self).__init__(parent)
        self.label = QLabel('Current Driving Time')
        self.time = QLabel(time)
        self._set_style()

    def _set_style(self):
        self.label.setObjectName('driveTimeLabel')
        self.time.setObjectName('driveTimeValue')
        self.time.setFixedHeight(int(get_height() * 0.15))
        self.layout.addWidget(self.time, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.label, alignment=Qt.AlignBottom)
        self.setStyleSheet(load_stylesheet('travel_styles.qss'))


class TravelInfoDriving(TravelInfo):
    left_drive_time: DriveTime = None
    right_driving_distance: DriveDistance = None

    def __init__(self, travel_info: dict = None, parent: QWidget = None):
        super(TravelInfoDriving, self).__init__(parent)
        self.initUI(travel_info=travel_info.get('info'))

    def initUI(self, travel_info: dict):
        self.left_drive_time = DriveTime(parent=self, time=travel_info.get('time'))
        self.right_driving_distance = DriveDistance(parent=self, distance=travel_info.get('distance'))
        self.set_sizes()
        self.set_positions()
        self.setStyleSheet(load_stylesheet('travel_styles.qss'))

    def set_sizes(self):
        self.left_drive_time.setMinimumWidth(int(get_width() * 0.35))
        self.right_driving_distance.setMinimumWidth(int(get_width() * 0.35))

    def set_positions(self):
        self.layout.addWidget(self.left_drive_time, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.right_driving_distance, alignment=Qt.AlignRight)


class FlightPriceContainer(BaseVContainer):
    bottom_label: QLabel = None
    flight_price: QLabel = None

    def __init__(self, parent: QWidget = None, price: float = None):
        super(FlightPriceContainer, self).__init__(parent)
        self.bottom_label = QLabel('Price')
        self.flight_price = QLabel(f"${price:.0f}")
        if price < 350:
            self.flight_price.setObjectName('flightPriceValueGood')
        elif price > 900:
            self.flight_price.setObjectName('flightPriceValueBad')
        else:
            self.flight_price.setObjectName('flightPriceValue')
        self.bottom_label.setObjectName('flightPriceLabel')
        self.flight_price.setFixedHeight(int(get_height() * 0.15))
        self.layout.addWidget(self.flight_price, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.bottom_label, alignment=Qt.AlignHCenter)


class FlightAbsoluteLocation(BaseVContainer):
    airport: QLabel = None

    def __init__(self, parent: QWidget = None, airport: str = None, time: datetime = None):
        super(FlightAbsoluteLocation, self).__init__(parent)
        self.airport = QLabel(airport)
        self.initUI()

    def initUI(self):
        self.airport.setObjectName('flightAbsoluteLocationAirport')
        self.layout.addWidget(self.airport)


class FlightSegment(BaseHContainer):
    flightOrigin: FlightAbsoluteLocation = None
    flightDestination: FlightAbsoluteLocation = None
    flightArrow: QLabel = None

    def __init__(self, parent: QWidget = None, flight_segment_info: dict = None):
        super(FlightSegment, self).__init__(parent)
        self.flightArrow = QLabel('→')
        self.flightArrow.setStyleSheet(" font-size: 8px; ")
        self.flightArrow.setFixedWidth(int(get_width() * 0.01))
        self.flightCommonInfo = BaseHContainer()
        self.initUI(flight_segment_info=flight_segment_info)

    def initUI(self, flight_segment_info: dict = None):
        self.flightOrigin = FlightAbsoluteLocation(
            parent=self,
            airport=flight_segment_info.get('departFrom'),
            time=parser.parse(flight_segment_info.get('departAt'))
        )
        self.flightDestination = FlightAbsoluteLocation(
            parent=self,
            airport=flight_segment_info.get('arriveIn'),
            time=parser.parse(flight_segment_info.get('arriveAt'))
        )
        self.layout.addWidget(self.flightCommonInfo, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.flightOrigin, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.flightArrow, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.flightDestination, alignment=Qt.AlignHCenter)


class WholeFlightInfo(BaseVContainer):
    flightSpecificInfo: FlightSegment = None
    flightCommonInfo = BaseHContainer = None

    def __init__(self, parent: QWidget = None, flight_segment_info: dict = None):
        super(WholeFlightInfo, self).__init__(parent)
        self.flightCommonInfo = BaseHContainer(parent=self)
        self.flightSpecificInfo = FlightSegment(parent=self, flight_segment_info=flight_segment_info)
        self.initUI(flight_segment_info)

    def initUI(self, flight_segment_info: dict = None):
        self.flightCommonInfo.layout.addWidget(QLabel(flight_segment_info.get('code')), alignment=Qt.AlignHCenter)
        self.flightSpecificInfo.setFixedHeight(int(get_height() * 0.1))
        self.layout.addWidget(self.flightSpecificInfo, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.flightCommonInfo, alignment=Qt.AlignVCenter)


class FlightSegments(BaseHContainer):
    def __init__(self, parent=None, flight_segments_info=None):
        super(FlightSegments, self).__init__(parent)
        self.initUI(flight_segments_info=flight_segments_info)

    def initUI(self, flight_segments_info):
        if type(flight_segments_info) == str and 'could not find flight info' in flight_segments_info:
            self.layout.addWidget(QLabel(flight_segments_info), alignment=Qt.AlignHCenter)
        else:
            for segment in flight_segments_info:
                self.layout.addWidget(
                    WholeFlightInfo(parent=self, flight_segment_info=segment),
                    alignment=Qt.AlignHCenter, stretch=1
                )


class FlightSegmentsInfo(BaseVContainer):
    direction: QLabel = None
    flights: FlightSegments = None

    def __init__(self, parent=None, flight_segments_info=None, direction=None):
        super(FlightSegmentsInfo, self).__init__(parent)
        self.initUI(flight_segments_info=flight_segments_info, direction=direction)

    def initUI(self, flight_segments_info, direction):
        self.direction = QLabel(direction)
        self.direction.setObjectName('flightDirection')
        self.flights = FlightSegments(parent=self, flight_segments_info=flight_segments_info)
        self.flights.setFixedHeight(int(get_height() * 0.15))
        self.layout.addWidget(self.flights, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.direction, alignment=Qt.AlignHCenter)


class TravelInfoFlying(TravelInfo):
    left_depart_flight: FlightSegmentsInfo = None
    middle_return_flight: FlightSegmentsInfo = None
    right_flying_price: FlightPriceContainer = None

    def __init__(self, parent: QWidget = None, travel_info: dict = None):
        super(TravelInfoFlying, self).__init__(parent)
        self.initUI(travel_info=travel_info.get('info'))

    def initUI(self, travel_info: dict = None):
        depart_date = parser.parse(travel_info.get('depart', [{}])[0].get('departAt', ''))
        return_date = parser.parse(travel_info.get('return', [{}])[0].get('departAt', ''))
        self.left_depart_flight = FlightSegmentsInfo(
            parent=self,
            flight_segments_info=travel_info.get('depart'),
            direction='Departing Flight(s) on ' + depart_date.date().strftime("%m/%d")
        )
        self.middle_return_flight = FlightSegmentsInfo(
            parent=self,
            flight_segments_info=travel_info.get('return'),
            direction='Returning Flight(s) on ' + return_date.date().strftime("%m/%d")
        )
        if 'could not' in str(travel_info.get('price')):
            self.right_flying_price = FlightPriceContainer(parent=self, price=float(0))
        else:
            self.right_flying_price = FlightPriceContainer(parent=self, price=float(travel_info.get('price')))
        self.set_sizes()
        self.set_positions()
        self.set_styles()

    def set_sizes(self):
        self.left_depart_flight.setFixedWidth(int(get_width() * 0.3))
        self.middle_return_flight.setFixedWidth(int(get_width() * 0.3))
        self.right_flying_price.setFixedWidth(int(get_width() * 0.08))

    def set_positions(self):
        self.layout.addWidget(self.left_depart_flight, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.middle_return_flight, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_flying_price, alignment=Qt.AlignRight)

    def set_styles(self):
        self.left_depart_flight.setObjectName('departing')
        self.middle_return_flight.setObjectName('returning')
        self.setStyleSheet(load_stylesheet('travel_styles.qss'))
