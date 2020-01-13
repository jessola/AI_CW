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
    stations = get_stations(station)

    # Check that the station exists
    if len(stations) < 0:
        error = '%s is not a station'
        return error

    return None
