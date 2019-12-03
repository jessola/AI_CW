import csv
from datetime import datetime


def parse_csv(filename, newline='\n'):
    """Parse a csv file full of train information and only return the relevant
     fields.
      
      Arguments:
          filename {str} -- Path to the csv file
      
      Yields:
          {List} -- Journeys with the fields id, date, loc, pla_a, pla_d, act_a,
        act_d.
      """

    # Define the relevant stations
    relevant_stops = [
        'NRCH',
        'DISS',
        'STWMRKT',
        'IPSWICH',
        'MANNGTR',
        'CLCHSTR',
        'CHLMSFD',
        'STFD',
        'LIVST',
    ]

    # Open the filename (csv extension can be included)
    filename = filename.replace('.csv', '')

    # Convert the times into 4 digit ints
    fmt_time = lambda time: int(time.replace(':', '')) if time != '' else None

    try:
        with open(filename + '.csv', newline=newline) as input_file:
            reader = csv.reader(input_file)

            for i, row in enumerate(reader):
                # Ignores the final row and header
                if len(row) > 1 and i != 0 and row[1] in relevant_stops:
                    yield ({
                        'id': row[0],
                        'date': datetime.strptime(row[0][:8], '%Y%m%d'),
                        'location': row[1],
                        'pla_d': fmt_time(row[3]),
                        'pla_a': fmt_time(row[2]),
                        'act_d': fmt_time(row[18]),
                        'act_a': fmt_time(row[16]),
                    })
    except:
        print('File does not exist.')


# a_list = (parse_csv('data/NRCH_LIVST_OD_a51_2019_1_1.csv'))

# for item in list(a_list)[:100]:
#     print(item['pla_a'], item['act_a'])
#     pass
