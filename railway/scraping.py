from bs4 import BeautifulSoup
import requests

def get_railway_stations():
  """Get a list of railway stations in Great Britain.
  
  Returns:
      {list} -- List of station names as dicts with their name and code.
  """
  
  stations = []  
  URL = 'https://web.archive.org/web/20121125233554/http://www.nationalrail.co.uk/stations/codes/'
  html = requests.get(URL).text
  soup = BeautifulSoup(html, 'html.parser')
  
  print(soup.select_one('table'))
  
  return stations


get_railway_stations()