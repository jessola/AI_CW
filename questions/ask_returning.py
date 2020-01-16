from random import choice


def ask_returning(context):
    """Prompts the user to specify whether or not they need to return.
  """

    options = [
        'Are you coming back as well?',
        'Would you like a return ticket?',
        'Shall I find you a return ticket?',
    ]

    # Check for context
    if context:
        dep_from = context['departing_from'].title() or None

        # Check for dep_from
        if dep_from:
            options.append(
                'Are you going back to {} afterwards?'.format(dep_from))
            options.append('Will you be returning to {}?'.format(dep_from))
            options.append(
                'Do you need a return ticket to {}?'.format(dep_from))
            options.append(
                'Shall I find you a return ticket to {}?'.format(dep_from))

    # Select a random question.
    return choice(options)
