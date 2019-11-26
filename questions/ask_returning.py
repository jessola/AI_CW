from random import choice

def ask_returning():
  """Prompts the user to specify whether or not they need to return.
  """

  options = [
    'Are you coming back as well?',
    'Would you like a return ticket?'
  ]

  # Select a random question.
  return choice(options)