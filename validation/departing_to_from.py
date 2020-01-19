from railway.station import get_stations, get_station

# Check whether


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
    if station.lower() == 'noriwch':
        suggested = 'Norwich'
        return suggested

    if station.lower() == 'manny':
        suggested = 'Manchester'
        return suggested

    if 'uea' in station.lower():
        suggested = 'Norwich'
        return suggested

    return suggested


# if __name__ == '__main__':
#     print(validate_dep_to_from('Nfsaklfjlfjdslf'))
