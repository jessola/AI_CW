import re


def validate_previous_delay(minutes, context=None):
    """Ensures that delay time is a number
      
      Arguments:
          minutes {str} -- Time as parsed from what the user has typed.
      """
    error = None

    # Check that there is a valid date string
    pattern = "[0-9]"
    fmt_time = re.search(pattern, time)
    extra = re.sub(pattern, '', time)

    if fmt_time is None:
        error = 'I can\'t understand what you mean by {}.'.format(time)

    return error