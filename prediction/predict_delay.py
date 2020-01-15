from datetime import datetime, timedelta

from .from_station import from_station


# Convert the actual station name into format required for algorithms
def name_to_id(station_name):
    stations = {
        'norwich': 'NRCH',
        'diss': 'DISS',
        'stowmarket': 'STWMRKT',
        'ipswich': 'IPSWICH',
        'manningtree': 'MANNGTR',
        'colchester': 'CLCHSTR',
        'chelmsford': 'CHLMSFD',
        'stratford': 'STFD',
        'london': 'LIVST',
    }

    if station_name.lower() not in stations.keys():
        return None

    return stations[station_name]


# Determine whether or not date is on weekday
IS_WEEKDAY = lambda d: 1 if d.weekday() > 4 else 0


def predict_delay(delay_from_prev, start, end, date):
    """Predict the delay based on a train journey from one station to another,
  accounting for the delay from the previous station and whether the journey
  is on a weekday or not.
  
  Arguments:
      delay_from_prev {int} -- Delay from previous station.
      start {str} -- Starting point.
      end {str} -- Destination.
      date[datetime] -- The journey's start date.
  
  Returns:
      int -- Delay
  """
    dep_from = name_to_id(start.lower())
    dep_to = name_to_id(end.lower())
    weekday = IS_WEEKDAY(date)

    prediction = from_station(dep_from).predict([[weekday, delay_from_prev]])

    return int(round(prediction[0]))


if __name__ == '__main__':
    station = 'ipswich'
    date = datetime.now() + timedelta(days=4)
    delay = 75

    print(
        'The delay on {} from {} when you arrived {} minutes late is approximately {} minutes.'
        .format(
            date.strftime('%D'),
            station.title(),
            delay,
            predict_delay(delay, station, 'fsf', date),
        ))
