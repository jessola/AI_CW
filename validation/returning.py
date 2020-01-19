def validate_ret(answer, context=None):
    error = None

    if answer.lower() not in ['yes', 'yeah', 'yep', 'no', 'nope', 'nah']:
        error = 'I\'m not sure what you mean. A simple yes or no is all I need.'

    return error
