from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re


def format_output(name):
    """Strips newlines and other extraneous artefacts from the output
    
    Arguments:
        name {str} -- Raw HTML output.
    """

    return re.sub('(\s{2,})|\[|\]', '', name)


def find_cheapest_ticket(
    dep_from,
    dep_to,
    dep_date={
        'condition': 'dep',
        'date': datetime.now()
    },
    ret_date=None,
):
    """Finds the cheapest train ticket for a specified journey.
      
      Arguments:
          dep_from {str} -- Departing from
          dep_to {str} -- Departing to
          dep_date {dict} -- Departure date and whether it's arrive before or depart after
          ret_date {dict} -- Return date and whether it's arrive before or depart after
      """

    BASE_URL = "http://ojp.nationalrail.co.uk/service/timesandfares"

    # Format the dates and times
    departure_date = dep_date['date'].strftime("%d%m%y")
    departure_time = dep_date['date'].strftime("%H%M")

    if ret_date:
        return_date = ret_date['date'].strftime("%d%m%y")
        return_time = ret_date['date'].strftime("%H%M")

    # Create new URL
    final_url = BASE_URL

    # Add the departing from & departing to to URL
    final_url += '/{}/{}'.format(dep_from, dep_to)

    # Add the departing date/time to the url
    final_url += '/{}/{}/{}'.format(departure_date, departure_time,
                                    dep_date['condition'])

    # Optionally add the return date/time to the url
    if ret_date:
        final_url += '/{}/{}/{}'.format(return_date, return_time,
                                        ret_date['condition'])

    html = requests.get(final_url).text

    # Set up the scraping
    soup = BeautifulSoup(html, "html.parser")

    # Get relevant information > FORMAT THESE LATER
    output_dep_date = datetime.strftime(dep_date['date'], '%d/%m/%y')
    output_dep_from = soup.select_one('td.from').next_element
    output_dep_to = soup.select_one(
        'td.to').next_element.next_element.next_element.next_element
    output_dep_time = soup.select_one('td.dep').next_element
    output_arr_time = soup.select_one('td.arr').next_element

    ## Get the single or return price
    if ret_date:
        output_price = (
            soup.select_one('label.opreturn span.label-text').next_element)
    else:
        output_price = re.sub(
            '([a-zA-Z]|\s)', '',
            soup.select_one('#buyCheapestButton span').next_element)

    return {
        'departure_date': format_output(output_dep_date),
        'departure_time': format_output(output_dep_time),
        'arrival_time': format_output(output_arr_time),
        'departing_from': format_output(output_dep_from),
        'departing_to': format_output(output_dep_to),
        'price': format_output(output_price)[1:],  # remove the currency symbol
        'ticket_type': "rtn" if ret_date is not None else 'sgl',
        'ticket_url': 'none',
        # 'returning': True if ret_date else False
    }
