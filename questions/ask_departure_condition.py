from random import choice

def ask_departure_condition():
  """Prompts the user to specify their departure condition, e.g. departing after or arriving before
  """

  options = [
    'Would you like to arrive before this time or depart after?',
    'After or before this time?',
  ]

  # Select a random question.
  return choice(options)