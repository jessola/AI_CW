import re


def validate_previous_delay(minutes, context=None):
    """Ensures that delay time is a number
      
      Arguments:
          minutes {str} -- Time as parsed from what the user has typed.
      """
    error = None

    # Check that there is a valid date string
    pattern = "[0-9]"
    fmt_minutes = re.search(pattern, minutes)
    extra = re.sub(pattern, '', minutes)

    if fmt_minutes is None:
        error = 'I can\'t understand what you mean by {}.'.format(minutes)

    return error