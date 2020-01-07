from .get_journeys import get_all_journeys
from datetime import datetime

# Arrival/Departure dates are currently just integers, so time differences need
# to be calculated with that in mind
to_minutes = lambda num: ((num // 100) * 60) + ((num % 100) % 60)

time_diff = lambda actual, planned: to_minutes(actual) - to_minutes(planned)

# Make sure the journey information is valid
invalid = lambda j: (j[3] and abs(j[3]) >= 300) or (j[4] and abs(j[
    4]) >= 300) or (j[5] and abs(j[5]) >= 300)


def at_station(station):
    """Returns the information about arrivals at and departures from a particular
  station between Norwich and London Liverpool Street. This information includes
  the previous station and how long it was delayed, as well as the planned
  arrival at and departure from the chosen station. Additional information
  includes the day of the week, and whether or not the journey was during peak
  times.
  
  The output of this is a dictionary that can contribute to the creation of a 
  prediction model. This dictionary has a 'data' member that is a 2-dimensional
  array and a 'values' member.
  
  Arguments:
      station {str} -- The target station.
  """
    if station == 'NRCH':
        raise ValueError('Cannot depart TO Norwich under the stipulations.')

    # Get all the journeys and reverse them, so it's easier to traverse
    all_journeys = list(get_all_journeys())
    all_journeys.reverse()

    # Prepare the state
    filtered_journeys = []  # The array that's returned in the end
    at_target_station = False  # Keeps track of the current station in the loop

    # print(2359 - 0000, time_diff(2359, 0000))
    for j in all_journeys:
        if not at_target_station:
            if j['location'] == station and (j['act_a']):
                day_of_week = j['date'].weekday()
                is_weekend = 1 if day_of_week > 4 else 0
                arr_delay = None
                dep_delay = None

                if j['act_a'] and j['pla_a']:
                    arr_delay = time_diff(int(j['act_a']), int(j['pla_a']))

                if j['act_d'] and j['pla_d']:
                    dep_delay = time_diff(int(j['act_d']), int(j['pla_d']))

                filtered_journeys.append([
                    day_of_week,
                    is_weekend,
                    arr_delay,
                    dep_delay,
                ])
                at_target_station = True
        else:
            delay_from_prev = None
            filtered_journeys[-1].insert(0, j['location'])

            if (j['act_d'] and j['pla_d']):
                delay_from_prev = time_diff(j['act_d'], j['pla_d'])
            filtered_journeys[-1].insert(3, delay_from_prev)

            at_target_station = False

    # for j in filtered_journeys:
    #     if j[0] != 'STFD':
    #         print(j)

    return [journey for journey in filtered_journeys if not invalid(journey)]
    # return
