from random import choice


def ask_other_stations(context=None):
    """Prompts the user to specify which other stations they will pass through
  """

    options = [
        'Which other stations are you passing through?',
        'What stations are you passing through?',
    ]

    # Check for context
    if context:
        # Check for dep_to
        if context['departing_to']:
            dep_to = context['departing_to'].title()
            options.append(
                'Which stations are you passing through on your way to {}?'.
                format(dep_to))
            options.append(
                'Okay, so which other stations are you passing through on you way to {}?'
                .format(dep_to))

    # Select a random question.
    return choice(options)
