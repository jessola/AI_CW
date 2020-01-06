from .get_journeys import get_all_journeys


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

    # Get all the journeys and reverse them, so it's easier to traverse
    all_journeys = list(get_all_journeys())
    all_journeys.reverse()

    # Prepare the state
    filtered_journeys = []  # The array that's returned in the end
    at_target_station = False  # Keeps track of the current station in the loop

    for journey in all_journeys:
        if not at_target_station:
            if journey['location'] == station and journey['act_d']:
                at_target_station = True
                filtered_journeys.append([
                    journey['pla_a'], journey['act_a'], journey['pla_d'],
                    journey['act_d']
                ])
        else:
            if journey['act_d']:
                filtered_journeys[-1].append(journey['location'])
                at_target_station = False

    for j in filtered_journeys:
        print(j)

    # return filtered_journeys
    # return
