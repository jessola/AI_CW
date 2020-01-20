from random import choice


def ask_starting(context=None):
    """Prompts the user to specify where they started their journey.
  """

    options = [
        'Where did you depart from?', 'Which station are you at right now',
        'What\'s the starting point of your journey?'
    ]

    # Check for context
    if context:
        # Check for dep_to
        if context['departing_to']:
            dep_to = context['departing_to'].title()
            options.append(
                'Which station are you beginning your journey to {} from?'.
                format(dep_to))
            options.append(
                'Okay, so you\'re going to {}. Where are you starting from?'.
                format(dep_to))

    # Select a random question.
    return choice(options)
