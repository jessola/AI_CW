from random import choice


def ask_departure_date():
    """Prompts the user to specify when they want to leave.
  """

    options = [
        'What day are you leaving?',
        'What is the date you\'re departing on?',
    ]

    # Select a random question.
    return choice(options)
