from random import choice
from datetime import datetime


def ask_departure_time(context=None):
    """Prompts the user to specify when they want to leave.
  """

    options = [
        'What time are you leaving?',
        'What time do you want to depart?',
    ]

    # Check for context
    if context:
        dep_date = context['departure_date'] or None
        dep_to = context['departing_to'] or None

        # Check for dep_top and/or dep_date
        if dep_date and dep_to:
            options.append('What time on {} are you going to {}?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D'), dep_to))
            options.append('What time on {} do you want to go to {}?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D'), dep_to))
            options.append('When on {} do you want to go to {}?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D'), dep_to))
            options.append('When on {} are you going to {}?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D'), dep_to))

        if dep_to:
            options.append('What time do you want to go to {}?'.format(dep_to))
            options.append('When are you going to {}?'.format(dep_to))

        if dep_date:
            options.append('When on {} are you leaving?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D'), ))
            options.append('What time on {} are you leaving?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D')))
            options.append('When on {} are you leaving?'.format(
                datetime.strptime(dep_date, '%d%m%y').strftime('%D')))

    # Select a random question.
    return choice(options)
