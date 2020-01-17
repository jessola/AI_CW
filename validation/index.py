from .departing_to_from import validate_dep_to_from, suggest_dep_to_from
from .returning import validate_ret
from .times import validate_time
from .dates import validate_date


def validate(value, option):
    # Departing from and departing to
    if option in ['departing_from', 'departing_to']:
        return validate_dep_to_from(value)

    # Returning was not 'yes' or 'no'
    if option == 'returning':
        return validate_ret(value)

    # Any dates
    if option in ['departure_date', 'return_date']:
        return validate_date(value)

    # Any times
    if option in ['departure_time', 'return_time']:
        return validate_time(value)

    return None


def suggest(value, option):
    # Departing from and to
    if option in ['departing_from', 'departing_to']:
        return suggest_dep_to_from(value)