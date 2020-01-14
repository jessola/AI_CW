from railway.station import get_stations


def validate_dep_to_from(station):
    """Checks that the stations the user wishes to travel between actually
    exist.
    
    Arguments:
        station {str} -- Station name as typed by the user.
    
    Returns:
        dict -- The error message
    """
    error = ''
    stations = get_stations(station.lower())

    # Check that the station exists
    if len(stations) < 1:
        error = '%s isn\'t a station' % station
        return error

    return None


# if __name__ == '__main__':
#     print(validate_dep_to_from('Nfsaklfjlfjdslf'))
