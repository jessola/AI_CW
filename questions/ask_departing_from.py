from random import choice

def ask_departing_from():
  """Prompts the user to specify where they wish to depart from.
  """

  options = [
    'Where would you like to depart from?',
    'What station are you leaving from?'
  ]

  # Select a random question.
  return choice(options)