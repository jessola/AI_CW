from random import choice

def ask_return_time():
  """Prompts the user to specify when they want to return.
  """

  options = [
    'When do you want to return?',
    'When do you want to come back?',
  ]

  # Select a random question.
  return choice(options)