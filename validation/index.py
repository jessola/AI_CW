from .departing_to_from import validate_dep_to_from, suggest_dep_to_from, validate_start_dest, valid_delay_stations
from .returning import validate_ret
from .times import validate_time
from .dates import validate_date
from .previous_delay import validate_previous_delay


def validate(value, option, context=None):
    # Departing from and departing to
    if option in ['departing_from', 'departing_to']:
        return validate_dep_to_from(value, context)

    # Start and Destination (Delay Prediction)
    if option in ['starting', 'destination']:
        return validate_start_dest(value, context)

    # Returning was not 'yes' or 'no'
    if option == 'returning':
        return validate_ret(value, context)

    # Any dates
    if option in ['departure_date', 'return_date']:
        return validate_date(value, context)

    # Any times
    if option in ['departure_time', 'return_time']:
        return validate_time(value, context)

    # Previous Delay
    if option == 'previous_delay':
        return validate_previous_delay(value, context)

    return None


def suggest(value, option, context=None):
    if context:
        context.update({'answering': option})

    # Departing from and to
    if option in ['departing_from', 'departing_to']:
        return suggest_dep_to_from(value, context)

    return None