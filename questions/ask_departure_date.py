from random import choice


def ask_departure_date(context=None):
    """Prompts the user to specify when they want to leave.
  """

    options = [
        'What day are you leaving?',
        'What is the date you\'re departing on?',
    ]

    # Check for context
    if context:
        dep_from = context['departing_from'].title() or None
        dep_to = context['departing_to'].title() or None
        # Check for dep_from and/or dep_to
        if dep_from and dep_to:
            options.append('What day are you going from {} to {}?'.format(
                dep_from, dep_to))

        if dep_from:
            options.append(
                'What day are you leaving from {}?'.format(dep_from))

        if dep_to:
            options.append('What day do you want to go to {}?'.format(dep_to))
            options.append('When are you going to {}?'.format(dep_to))

    # Select a random question.
    return choice(options)
