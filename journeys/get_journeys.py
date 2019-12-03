from .parse_csv import parse_csv


def get_all_journeys(newline='\n'):
    """Return all of the journey information. That's from January 2017 to May 2019
  from Norwich to London Liverpool Street.
  
  Keyword Arguments:
      newline {str} -- The delimeter to use when parsing the csv files. This is 
  necessary because csv files work differently on different  (default: {'\n'})
  operating systems.
  """

    BASE_PATH = 'data/NRCH_LIVST_OD_a51'

    # Loop through the months in the years 2017 - 2019, and open corresponding
    # csv files.
    for year in range(2017, 2020):
        for month in range(1, 13):
            full_path = '{}_{}_{}_{}'.format(BASE_PATH, year, month, month)

            for item in parse_csv(full_path, newline):
                yield item


def get_journeys(callback_func, newline='\n'):
    """Return all journeys matching a specific predicate, specified in a 
      callback function.
      
      Arguments:
          callback_func {function} -- Function that returns a bool.
          newline {function} -- Delimeter in the csv files.
      """

    for item in get_all_journeys(newline=newline):
        if callback_func(item):
            yield item
