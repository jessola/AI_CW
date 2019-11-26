from random import choice

def ask_num_adults():
  """Prompts the user to specify the number of adults travelling.
  """

  options = [
    'How many adults are you going with?',
    'How many adults are going?',
    'How many adults tickets do you need?',
  ]

  # Select a random question.
  return choice(options)