from random import choice


def ask_num_children():
    """Prompts the user to specify the number of children travelling.
  """

    options = [
        "How many children are you going with?",
        "How many children are going?",
        "How many child tickets do you need?",
    ]

    # Select a random question.
    return choice(options)

