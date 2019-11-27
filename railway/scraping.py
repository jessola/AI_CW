from bs4 import BeautifulSoup
import requests


def get_railway_stations():
    """Get a list of railway stations in Great Britain.
  
  Returns:
      {list} -- List of station names as dicts with their name and code.
  """

    URL = "https://web.archive.org/web/20121125233554/http://www.nationalrail.co.uk/stations/codes/"
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")

    # Select the names and codes
    raw_names = soup.select("td.h, td.hospital")
    raw_codes = soup.select("td.s, td.station")

    # Format them nicely
    names = [element.next_element.next_element for element in raw_names]
    codes = [element.next_element for element in raw_codes]

    # Return an array of dictionaries containing each station name and code
    return [{"name": name, "code": codes[names.index(name)]} for name in names]
