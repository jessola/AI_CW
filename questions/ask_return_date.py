from random import choice


def ask_return_date():
    """Prompts the user to specify when they want to return.
  """

    options = [
        'When do you want to return?',
        'When are you coming back?',
    ]

    # Select a random question.
    return choice(options)
