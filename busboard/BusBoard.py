import requests
from pprint import pprint 


def departure_list(postcode):

    pc_coords = get_pc_coords(postcode)
    #pprint(pc_coords)

    atco_codes = get_bus_stops(pc_coords, 2)
    #pprint(atco_codes)

    departure_list = []
    for stop in atco_codes:
        live_departure = get_live_bus_times(stop)

        #pprint(live_departure)

        stop_departure = live_departure['line'] + ' - ' + live_departure['direction'] + ' - Expected at: ' + live_departure['expected_departure_time']

        departure_list.append(stop_departure)

    return departure_list


def get_pc_coords(user_postcode):
    """
    Return the latitude and logitude of the given postcode as a tuple
    """
    #user_postcode = "GU213AF"
    response = requests.get('https://api.postcodes.io/postcodes/'+user_postcode)
    
    response_json = response.json()

    pc_coords = (response_json['result']['latitude'] , response_json['result']['longitude'] )

    return pc_coords


def get_bus_stops(pc_coords, num_stops = 2):
    """
    Return a list object with the atcocodes of the nearest n stops
    """
    query = f"?lat={pc_coords[0]}&lon={pc_coords[1]}&type=bus_stop"
    authentication = f"&app_id=feaa5797&app_key=41c7a00e1e7ef0502bfee7be099f17fe"
    response = requests.get('http://transportapi.com/v3/uk/places.json'+ query + authentication)
    response_json = response.json()

    #pprint(response_json)

    all_stops = response_json['member']
    requested_stops = all_stops[0:num_stops]
    
    requested_stops_atco = [stop['atcocode'] for stop in requested_stops]

    return requested_stops_atco


def get_live_bus_times(atcocode):

    authentication = f"app_id=feaa5797&app_key=41c7a00e1e7ef0502bfee7be099f17fe"
    parameters = "&group=no&limit=1&nextbuses=yes"
    response = requests.get('http://transportapi.com/v3/uk/bus/stop/' + atcocode + '/live.json?' + authentication + parameters)
    response_json = response.json()

    live_departure = response_json['departures']

    return live_departure['all'][0]

    
# Call main() when running as script
if __name__ == '__main__':
    main()

