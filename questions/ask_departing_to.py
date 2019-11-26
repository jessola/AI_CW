from random import choice

def ask_departing_to():
  """Prompts the user to specify their destination.
  """

  options = [
    'Where are you travelling to?',
    'Where do you want to go?',
    'Where to?',
    'Where are you going?'
  ]

  # Select a random question.
  return choice(options)