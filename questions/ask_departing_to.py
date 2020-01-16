from random import choice


def ask_departing_to(context=None):
    """Prompts the user to specify their destination.
  """
    options = [
        'Where are you travelling to?', 'Where do you want to go?',
        'Where to?', 'Where are you going?'
    ]

    # Check for context
    if context:
        # Departing From
        if context['departing_from']:
            dep_from = context['departing_from'].title()
            options.append('From {} to where?'.format(dep_from))
            options.append('Where do you want to go from {}?'.format(dep_from))

    # Select a random question.
    return choice(options)
