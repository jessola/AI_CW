from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta


def find_cheapest_ticket(dep, arr, dep_date, arr_date):
    """Finds the cheapest train ticket for a specified journey.
      
      Arguments:
          dep {str} -- Departing from
          arr {str} -- Arriving at
          dep_date {datetime} -- Departure Date/Time (intended)
          arr_date {datetime} -- Arrival Date/Time (intended)
      """

    BASE_URL = "http://ojp.nationalrail.co.uk"

    # Format the dates and times
    departure_date = dep_date.strftime("%d%m%y")
    departure_time = dep_date.strftime("%H%M")
    arrival_date = None
    arrival_time = None

    # Create new URL
    final_url = "{}/service/timesandfares/{}/{}/{}/{}/dep".format(
        BASE_URL, dep, arr, departure_date, departure_time
    )
    html = requests.get(final_url).text

    # Set up the scraping
    soup = BeautifulSoup(html, "html.parser")

    # Get relevant information > FORMAT THESE LATER
    output_from = soup.select_one('td.from').next_element
    output_dep_time = soup.select_one('td.dep').next_element
    output_arr_time = soup.select_one('td.arr').next_element
    output_price = soup.select_one('label.opsingle').next_element.next_element.next_element

    print(
        soup.select_one('label.opsingle', text=True))

    return {
        'departure_date': None,
        'departure_time': output_dep_time,
        'arrival_time': output_arr_time,
        'from': output_from,
        'to': None,
        'price': output_price
    }

find_cheapest_ticket(
        "Norwich", "Portsmouth", datetime(2019, 11, 20), datetime(2019, 11, 21)
    )
