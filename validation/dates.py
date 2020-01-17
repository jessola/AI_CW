from datetime import datetime
import re


def validate_date(date):
    """Validates date strings, ensuring date is in 2020 and not in the past as
  this is what's required for the web scraping to work properly.
  
  Arguments:
      date {str} -- Date string in the format DDMMYY
  """
    error = None

    pattern = "(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])20"
    fmt_date = re.search(pattern, date)
    extra = re.sub(pattern, '', date)

    if not fmt_date or len(extra.strip()) > 0:
        error = 'I don\'t think {} is a valid date'.format(date)
        return error

    # February Check
    if int(fmt_date[0][2:4]) == 2 and int(fmt_date[0][0:2]) > 29:
        error = 'February only has 29 days this year.'
        return error

    # Date check
    if datetime.strptime(fmt_date[0], "%d%m%y") < datetime.now():
        error = 'Please don\'t pick a date in the past.'
        return error

    return None
