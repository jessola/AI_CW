from mongoengine import *

from railway.scraping import get_railway_stations

# Connect to the database
connect(
    host=
    "mongodb://group_ten:group10@ds037611.mlab.com:37611/railwaystations?retryWrites=false"
)


class Station(Document):
    name = StringField(max_length=50)
    code = StringField(max_length=3)
    aliases = ListField(StringField(max_length=50))


# DO NOT call this method unless you wish to reset the station information
def init_stations():
    """Populates the station collection with all of the stations in GB.
    Should only be done once.
    """

    for station in get_railway_stations():
        add_station(station["name"], station["code"])


# Method should not typically be used externally
def add_station(name, code, aliases=[]):
    """Adds a unique station to the collection of Railway Stations
      
      Arguments:
          name {str} -- The official name of the station.
          code {str} -- The station code.
      
      Keyword Arguments:
          aliases {list} -- Other names or misspellings of the station (default: {[]}).
      """
    # Check that the station is not already present
    if len(Station.objects(name__iexact=name)) > 0:
        return

    # Maybe validate codes and aliases

    # Add the new station
    s = Station(name=name, code=code.upper(), aliases=aliases)
    s.save()


def get_all_stations():
    """Gets all station documents from the database. This includes the station 
    name, code and any of its aliases.
    
    Returns:
        {list} -- List of the station objects.
    """

    return Station.objects


def get_stations(name):
    """Get all the stations whose names contain the input parameter.
    
    Arguments:
        name {str} -- Name to search for
    
    Returns:
        {list} -- All stations whose name contains the input parameter.
    """

    return Station.objects(name__icontains=name)


def get_station(name):
    """Get station whose name is equal to the input parameter.
    
    Arguments:
        name {str} -- Name to search for
    
    Returns:
        {Station} -- Matching station or none
    """

    return Station.objects(name__iexact=name)


def get_station_by_code(code):
    """Gets a Station document with the given code.
    
    Arguments:
        code {str} -- The station code of the desired station.
    
    Returns:
        {Station} -- Station object.
    """

    return Station.objects(code=code)[0]
