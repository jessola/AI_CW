from .departing_to_from import validate_dep_to_from
from .returning import validate_ret


def validate(value, option):
    # Departing from and departing to
    if option in ['departing_from', 'departing_to']:
        return validate_dep_to_from(value)

    # Returning was not 'yes' or 'no'
    if option == 'returning':
        return validate_ret(value)

    return None
