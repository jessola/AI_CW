import re


def validate_time(time, context=None):
    """Ensures that times are formatted properly, i.e. 2pm should be 1400.
      
      Arguments:
          time {str} -- Time as parsed from what the user has typed.
      """
    error = None

    # Check that there is a valid date string
    pattern = "([0-1][0-9]|[2][0-3])[0-5][0-9]"
    fmt_time = re.search(pattern, time)
    extra = re.sub(pattern, '', time)

    if fmt_time is None or len(extra.strip()) > 0:
        error = 'I can\'t understand what you mean by {}.'.format(time)

    return error
