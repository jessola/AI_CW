from railway.station import get_stations, get_station

# Valid stations for delay prediction
valid_delay_stations = [
    'norwich',
    'diss',
    'stowmarket',
    'ipswich',
    'manningtree',
    'colchester',
    'chelmsford',
    'stratford',
    'london liverpool street',
]


def format_stations(stations):
    try:
        matched_stations = [str(s.name) for s in stations]
        stations_string = ''

        # There are lots of possibilities
        if len(matched_stations) > 5:
            stations_string = ', '.join(matched_stations[0:5])
            stations_string += ' or {} others'.format(len(stations) - 5)
            return stations_string

        if len(matched_stations) >= 2:
            last_two = matched_stations[-2:]
            matched_stations = matched_stations[:-2]

            if len(matched_stations) > 0:
                stations_string += ', '.join(matched_stations)

                stations_string = ', '.join(
                    [stations_string, ' or '.join(last_two)])
            else:
                stations_string = ' or '.join(last_two)

        return stations_string

    except Exception as e:
        print(str(e))


def validate_dep_to_from(station, context=None):
    """Checks that the stations the user wishes to travel between actually
    exist.
    
    Arguments:
        station {str} -- Station name as typed by the user.
    
    Returns:
        dict -- The error message
    """
    error = ''
    stations = get_stations(station.lower())

    # Many stations match
    if len(stations) > 1 and not get_station(station):
        error = 'There\'s lots of stations you could mean when you say "{}".'.format(
            station)
        error += ' You could mean ' + format_stations(stations) + '.'

        return error

    # Check that the station exists
    if len(stations) < 1:
        error = '%s isn\'t a station' % station
        return error

    if context:
        dep_from = context['departing_from'] or None
        dep_to = context['departing_to'] or None

        if (dep_from and station.lower() == dep_from.lower()) or (
                dep_to and station.lower() == dep_to.lower()):
            error = 'Sorry but I don\'t think there\'ll be any journeys from {} to {}'.format(
                station.title(), station.title())
            return error

    return None


def suggest_dep_to_from(station, context=None):
    """User didn't exactly enter a station, but it is possible to guess what
    they might have meant.
    
    Arguments:
        station {str} -- Input station from the user.
    
    Returns:
        str -- Suggested station, if there is one.
    """
    suggested = None

    # TODO: proper spelling validation
    if station.lower() in ['noriwch', 'uea', 'norrich']:
        suggested = {
            'message': 'When you say "%s", do you mean Norwich?' % station,
            'value': 'Norwich',
            'original': station.lower(),
        }
        return suggested

    if station.lower() == 'manny':
        suggested = {
            'message': 'When you say "%s", do you mean Manchester?' % station,
            'value': 'Manchester',
            'original': station.lower(),
        }
        return suggested

    # Handle details being resubmitted without being formally retracted
    try:
        if context:
            dep_from = context['departing_from'] or None
            dep_to = context['departing_to'] or None

            # Departing From
            if context['answering'] == 'departing_from' and dep_from:
                suggested = {
                    'message':
                    'Are you sure you want to depart from {} instead of {}?'.
                    format(station.title(), dep_from.title()),
                    'value':
                    station,
                    'original':
                    None,
                }

            # Departing To
            if context['answering'] == 'departing_to' and dep_to:
                suggested = {
                    'message':
                    'Are you sure you want to go to {} instead of {}?'.format(
                        station.title(), dep_from.title()),
                    'value':
                    station
                }
    except Exception as e:
        print(str(e))

    return suggested


def validate_start_dest(station, context=None):
    """Checks that the stations the user wishes to travel between actually
    exist. Also check that they are for journies between Norwich and London
    Liverpool Street.
    
    Arguments:
        station {str} -- Station name as typed by the user.
    
    Returns:
        dict -- The error message
    """

    # Perform default station check
    if validate_dep_to_from(station):
        return validate_dep_to_from(station)

    # Make sure station is valid
    if station.lower() not in valid_delay_stations:
        return 'I can only help you if you are travelling between Norwich and London Liverpool Street, I\'m afraid.'

    return None


# if __name__ == '__main__':
#     print(validate_dep_to_from('Nfsaklfjlfjdslf'))
