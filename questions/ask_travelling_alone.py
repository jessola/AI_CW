from random import choice

def ask_travelling_alone():
  """Prompts the user to specify whether or not they are travelling alone.
  """

  options = [
    'Is it just you?',
    'Are you travelling alone?',
    'Are you going by yourself?',
    'Just the one ticket, right?'
  ]

  # Select a random question.
  return choice(options)