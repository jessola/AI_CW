from random import choice


def ask_return_time():
    """Prompts the user to specify when they want to return.
  """

    options = [
        'What time do you want to return?',
        'What time are you coming back?',
    ]

    # Select a random question.
    return choice(options)
