import re
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


def get_station_by_alias(alias):
    """Get the station based on any of its aliases
    
    Arguments:
        alias {str} -- Another name or mispelling of the station
    
    Returns:
        str -- The actual name of the station
    """
    if not alias:
        return None

    try:
        station = Station.objects(aliases__icontains=alias.lower())[0] or None

        if not station:
            return
        else:
            return station['name'].title()
    except Exception as e:
        print(str(e))
        return None


def add_alias(station, new_alias):
    """Adds a new alias for a given station.
    
    Arguments:
        station {str} -- Name of the station
        new_alias {str} -- New alias for the station
    """
    if not new_alias:
        return

    target_station = Station.objects(name__icontains=station)[0]

    if target_station and new_alias.lower() not in target_station['aliases']:
        target_station['aliases'].append(new_alias.lower())
        target_station.save()


def get_station_by_code(code):
    """Gets a Station document with the given code.
    
    Arguments:
        code {str} -- The station code of the desired station.
    
    Returns:
        {Station} -- Station object.
    """

    return Station.objects(code=code)[0]


def find_most_similar(user_input):
    """Finds the station most similar to what was written, or none
    
    Arguments:
        station {str} -- The search string
    
    Returns:
        str -- Name of the station most similar
    """
    user_input = user_input.lower()
    first = user_input[0]

    # Subset of all stations that start with the first typed letter
    subset = [
        s['name'].lower() for s in get_stations(first)
        if s['name'][0].lower() == first
    ]

    lhs = re.sub('[^a-zA-Z]', '', user_input)
    lhs = re.sub('[aeiou]', '', lhs)

    if len(subset) == 0:
        return None

    # Check for exact matches
    for station in subset:
        rhs = re.sub('[^a-zA-Z]', '', station)
        rhs = re.sub('[aeiou]', '', rhs)

        if lhs in rhs:
            return station.title()

    # More obscure matches
    for station in subset:
        lhs = re.sub('[^a-zA-Z]', '', user_input)
        rhs = re.sub('[^a-zA-Z]', '', station)
        # rhs = re.sub('[aeiou]', '', rhs)

        marked_letters = []
        matches = 0
        misses = 0

        for i, letter in enumerate(rhs):
            try:
                if i <= 9:
                    # Check which consonants appear in both
                    if letter not in marked_letters:
                        if letter in lhs:
                            matches += 1
                        else:
                            misses += 1

                    # Add it to marked list
                    if letter not in marked_letters:
                        marked_letters.append(letter)
            except Exception as e:
                print(str(e))

        # Check the ratio & conditionally return the station
        try:
            if matches / (matches + misses) > 0.8:
                return station.title()
        except Exception as e:
            print(str(e))

    return None


if __name__ == '__main__':
    print(find_most_similar(input('Enter a station:\t')))
