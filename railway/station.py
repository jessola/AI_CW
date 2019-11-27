from mongoengine import *


# Connect to the database
connect(
    host="mongodb://group_ten:group10@ds037611.mlab.com:37611/railwaystations?retryWrites=false"
)


class Station(Document):
    name = StringField(max_length=50)
    code = StringField(max_length=3)
    aliases = ListField(StringField(max_length=50))


def add_station(name, code, aliases=[]):
    """Adds a unique station to the collection of Railway Stations
      
      Arguments:
          name {str} -- The official name of the station.
          code {str} -- The station code.
      
      Keyword Arguments:
          aliases {list} -- Other names or misspellings of the station (default: {[]}).
      """
    # Check that the station is not already present
    if len(Station.objects(name=name.lower())) > 0:
        return

    # Maybe validate codes and aliases
    for alias in aliases:
        alias = alias.lower()

    # Add the new station
    s = Station(name=name.lower(), code=code.upper(), aliases=aliases)
    s.save()

