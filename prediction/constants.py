from joblib import load
from datetime import datetime, timedelta


# Convert the actual station name into format required for algorithms
def name_to_id(station_name):
    stations = {
        'norwich': 'norw',
        'diss': 'diss',
        'stowmarket': 'stow',
        'ipswich': 'ipsw',
        'manningtree': 'mann',
        'colchester': 'colc',
        'chelmsford': 'chel',
        'stratford': 'stfd',
        'london': 'lliv',
    }

    if station_name.lower() not in stations.keys():
        return None

    return stations[station_name.lower()]


# Get the usual inter-station travel time
def station_to_station_time(a, b):
    times = {
        'norwich_diss': 17,
        'norwich_ipswich': 33,
        'diss_stowmarket': 12,
        'diss_ipswich': 21,
        'stowmarket_ipswich': 12,
        'ipswich_manningtree': 11,
        'ipswich_london': 57,
        'manningtree_colchester': 10,
        'colchester_chelmsford': 19,
        'colchester_london': 51,
        'colchester_stratford': 42,
        'chelmsford_stratford': 25,
        'stratford_london': 10,
    }

    # London Liverpool Street edge case
    if b.lower() == 'london liverpool street':
        b = 'london'

    key = '{}_{}'.format(a.lower(), b.lower())
    if key not in times.keys():
        return None

    return times[key]


# Return the interstation travel times and the total travel time
def get_travel_times(*stops):
    info = {'stop_times': [], 'total': 0}

    if len(stops) < 2:
        return None

    try:
        for i in range(1, len(stops)):
            time = station_to_station_time(stops[i - 1], stops[i])
            info['stop_times'].append(time)
            info['total'] += time

        return info
    except:
        return None


# Load in a prediction model
def model(name, dep=True):
    prefix = 'prediction/models'

    try:
        return load('{}/{}_{}.joblib'.format(
            prefix,
            name_to_id(name),
            'dep' if dep else 'arr',
        ))
    except:
        return None


# Predict stuff
def make_prediction(start, delay, *stations):
    current_time = start  # Keeps track of actual the arrival/departure times
    planned_time = start  # Keeps track of actual the arrival/departure times
    dep_delays = [delay]
    info = []

    stops = get_travel_times(*stations)['stop_times']

    # # London Liverpool Street edge case
    # for station in stations:
    #     if station.lower() == 'london liverpool street':
    #         station = 'london'

    for i, station in enumerate(stations[1:]):
        # London edge case
        if station.lower() == 'london liverpool street':
            station = 'london'

        arr_pred = model(station, False).predict([[1, dep_delays[-1]]])[0]
        dep_pred = None
        if station.lower() not in ['london', 'london liverpool street']:
            dep_pred = model(station).predict([[1, dep_delays[-1]]])[0]

        # Calculate the new resultant delay
        if dep_pred:
            dep_delays.append(dep_pred - arr_pred)

        current_time += timedelta(minutes=stops[i] + arr_pred)
        planned_time += timedelta(minutes=stops[i])

        arr_time = current_time.strftime('%H:%M')
        pla_time = planned_time.strftime('%H:%M')

        # Calculate the delay rounded to the nearest minute
        act = datetime.strptime(arr_time, '%H:%M')
        pla = datetime.strptime(pla_time, '%H:%M')
        delay = int((act - pla).total_seconds() / 60)
        location = 'London Liverpool Street' if station.lower(
        ) == 'london' else station.title()

        info.append({
            'location': location,
            'pla_a': pla_time,
            'act_a': arr_time,
            'del': delay,
        })

    # print(current_time - start)
    # print(dep_delays)

    return info


if __name__ == '__main__':
    print(
        make_prediction(
            datetime.now(),
            5,
            # 'norwich',
            'diss',
            # 'stowmarket',
            'ipswich',
            'manningtree',
            'colchester',
            'chelmsford',
            # 'stratford',
            # 'london',
        ))
