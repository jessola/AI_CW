from mongoengine import *

STABLE = False  # Ensures current stations not overwritten if this file is run

# Connect to the database
connect(host="mongodb://group_ten:group10@ds037611.mlab.com:37611/railwaystations?retryWrites=false")


class Station(Document):
    name = StringField(max_length=50)
    aliases = ListField(StringField(max_length=50))


def add_station(name, aliases=[]):
      """Adds a unique station to the collection of Railway Stations
      
      Arguments:
          name {str} -- The official name of the station.
      
      Keyword Arguments:
          aliases {list} -- Other names or misspellings of the station (default: {[]}).
      """
      
      # Check that the station is not already present
      if len(Station.objects(name=name)) > 0:
            return
          
      # Maybe validate aliases
          
      # Add the new station
      
    
# Create some test stations
s1 = Station(name='Norwich', aliases=['Norrich'])
s1.save()

# Populate the database with stations
# Don't run this file unless you want to re-initialise the stations
if not STABLE:
  for station in Station.objects:
        print(station.name)
