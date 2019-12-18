from amadeus import Client as amadeus_Client
from helpers.config import (
    get_amadeus_keys, get_maps_key, get_resort_coordinates, get_origin_coordinates,
    get_airlines_pref, get_origin_airport, get_resort_airport_prefs, get_resort_driving
)
from googlemaps import Client as gmaps_Client
from datetime import timedelta, date
from pprint import pprint


def get_travel_info(resort):
    if get_resort_driving(resort):
        return {
            'mode': 'driving',
            'info': _get_driving_to_resort_data(resort)
        }
    return {
        'mode': 'flying',
        'info': _get_flying_to_resort_data(resort)
    }


def _get_driving_to_resort_data(resort):
    cli = _get_gmaps_client()
    resort_lat, resort_lon = get_resort_coordinates(resort)
    origin_lat, origin_lon = get_origin_coordinates()
    res = cli.directions(
        origin=''.join([origin_lat, ',', origin_lon]),
        destination=''.join([resort_lat, ',', resort_lon]),
        units='imperial'
    )
    return {
        'distance': _get_drive_distance(res),
        'time': _get_drive_time(res)
    }


def _get_flying_to_resort_data(resort):
    prefs = _get_flight_prefs(resort)
    flights_list = _in_two_weekends_flights(prefs)
    print(flights_list)  # TODO - change to logging
    return flights_list


def _get_common_flight_info(segments):
    massaged_segments = []
    for seg in segments:
        flight_info = seg.get('flightSegment')
        flight_departs = flight_info.get('departure').get('at')
        flight_depart_airport = flight_info.get('departure').get('iataCode')
        flight_arrives_airport = flight_info.get('arrival').get('iataCode')
        flight_arrives = flight_info.get('arrival').get('at')
        flight_duration = flight_info.get('duration', 'unknown duration')
        try:
            flight_massaged_dur = flight_duration.split('T')[1]
        except IndexError:
            flight_massaged_dur = flight_duration
        massaged_segments.append({
            'departFrom': flight_depart_airport,
            'departAt': flight_departs,
            'arriveIn': flight_arrives_airport,
            'arriveAt': flight_arrives,
            'duration': flight_massaged_dur
        })
    return massaged_segments


def _get_best_flight_depart_info(best_flight_service_data):
    segments = best_flight_service_data[0].get('segments')
    return _get_common_flight_info(segments)


def _get_best_flight_return_info(best_flight_service_data):
    segments = best_flight_service_data[1].get('segments')
    return _get_common_flight_info(segments)


def _get_best_flight(candidate_flights):
    best_price = float(10000000000)  # TODO - better way + logging
    for flight in candidate_flights:
        actual_data = flight.get('offerItems')[0]
        total_price = float(actual_data.get('price').get('total'))
        if not total_price < best_price:
            continue
        best_price = total_price
        best_flight_so_far = actual_data
    print(best_flight_so_far)
    return {
        'depart': _get_best_flight_depart_info(best_flight_so_far.get('services')),
        'return': _get_best_flight_return_info(best_flight_so_far.get('services')),
        'price': best_price
    }


def _in_two_weekends_flights(prefs):
    am_cli = prefs.get('amadeus_cli')
    thursday, sunday = _get_travel_dates()
    try:
        flights = am_cli.shopping.flight_offers.get(
            origin=prefs.get('orig_airport'),
            destination=prefs.get('res_airpot'),
            departureDate=thursday,
            returnDate=sunday,
            nonStop=prefs.get('nonstop', False),
            includeAirlines=prefs.get('airlines', 'UA'),
            currency='USD'
        )
        best_flight = _get_best_flight(flights.data)
    except Exception as e:
        print(e)  # TODO - logging
        return {
            'depart': "could not find flight info for departure",
            'return': "could not find flight info for return",
            'price': "could not find flight price"
        }
    return best_flight


def _get_drive_distance(maps_response):
    """
    from the gmaps response object, extract the driving distance
    """
    try:
        return maps_response[0].get('legs')[0].get('distance').get('text')
    except Exception as e:
        print(e)
        return 'unknown distance'


def _get_drive_time(maps_response):
    """
    from the gmaps response object, extract the driving time
    """
    try:
        text = maps_response[0].get('legs')[0].get('duration').get('text')
        return text
    except Exception as e:
        print(e)  # TODO - logging
        return 'unknown duration'


def _get_gmaps_client():
    return gmaps_Client(key=get_maps_key())


def _get_amadeus_client():
    key, secret = get_amadeus_keys()
    return amadeus_Client(
        hostname='production',  # TODO - add switch for nonprod
        client_id=key,
        client_secret=secret
    )


def _get_flight_prefs(resort_name):
    airlines = get_airlines_pref()
    origin_airport = get_origin_airport()
    resort_airport, nonstop_only = get_resort_airport_prefs(resort_name)
    cli = _get_amadeus_client()
    return {
        'nonstop': nonstop_only,
        'airlines': airlines,
        'orig_airport': origin_airport,
        'res_airpot': resort_airport,
        'amadeus_cli': cli
    }


def _get_travel_dates():
    today = date.today()
    if today.weekday() != 3:
        this_thursday_delta = (3 - today.weekday()) % 7
        this_thursday = date.today() + timedelta(days=this_thursday_delta)
    else:
        this_thursday = today
    two_weeks_thursday = this_thursday + timedelta(days=14)
    two_weeks_sunday = two_weeks_thursday + timedelta(days=3)  # TODO - logging
    return two_weeks_thursday.strftime("%Y-%m-%d"), two_weeks_sunday.strftime("%Y-%m-%d")

# TODO
# this is hacky and should be removed once flight UI is complete
def _build_flight_strings(flight_info):
    print(flight_info)
    flight_dep_str = flight_info['depart']
    flight_arr_str = flight_info['return']
    flight_price_str = flight_info['price']
    if flight_dep_str != 'could not find flight info for departure':
        flight_dep_str = "flight departs: " + ''.join([str(x.items()) for x in flight_info.get('depart')])
    if flight_arr_str != 'could not find flight info for return':
        flight_arr_str = "flight arrives: " + ''.join([str(x.items()) for x in flight_info.get('return')])
    if flight_price_str != 'could not find flight price':
        flight_price_str = "flight price: $" + str(flight_info.get('price'))
    return {
        'depart': flight_dep_str,
        'return': flight_arr_str,
        'price': flight_price_str
    }