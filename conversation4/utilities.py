from .fact_types import *


def return_fact(name, value=None, **kwargs):
    """Returns the fact subclass corresponding to the name input.
      
      Arguments:
          name {str} --  Name of the fact subclass in snake case.
          value {str} -- Value of the fact
      
      Keyword Arguments:
          kwargs {dict} -- Additional arguments (default: {dict()})
      """
    if name == 'departing_from':
        return DepartingFrom(value)

    if name == 'departing_to':
        return DepartingTo(value)

    if name == 'departure_date':
        return DepartureDate(value)

    if name == 'departure_time':
        return DepartureTime(value)

    if name == 'returning':
        answer = True if value.lower()[0] == 'y' else False
        return Returning(answer)

    if name == 'return_date':
        return ReturnDate(value)

    if name == 'return_time':
        return ReturnTime(value)

    if name == 'previous_delay':
        return PreviousDelay(value)

    return None
