from random import choice


def ask_previous_delay(context=None):
    """Prompts the user to specify how long their train has been delayed.
  """

    options = [
        'How long have you been waiting for?',
        'How long has your train been delayed?',
        'What\'s the length of the delay?',
        'How many minutes have you been delayed for?',
    ]

    # Check for context
    if context:
        # Check for dep_to
        if context['departing_from']:
            dep_from = context['departing_from'].title()
            options.append(
                'How long have you been stuck in {}?'.format(dep_from))

    # Select a random question.
    return choice(options)
