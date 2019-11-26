from random import choice

def ask_departure_time():
  """Prompts the user to specify when they want to leave.
  """

  options = [
    'When are you leaving?',
    'What time do you want to depart?',
  ]

  # Select a random question.
  return choice(options)