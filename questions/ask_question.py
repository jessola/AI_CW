from .ask_departing_from import ask_departing_from
from .ask_departing_to import ask_departing_to
from .ask_departure_condition import ask_departure_condition
from .ask_departure_date import ask_departure_date
from .ask_departure_time import ask_departure_time
from .ask_num_adults import ask_num_adults
from .ask_num_children import ask_num_children
from .ask_returning import ask_returning
from .ask_return_date import ask_return_date
from .ask_return_time import ask_return_time
from .ask_travelling_alone import ask_travelling_alone


def ask_question(topic):
    """Prompts the user to give details about the chosen topic.
  
  Arguments:
      topic {str} -- What the question relates to e.g. 'departure time'.
  """

    question = ""

    # Switch
    if topic == "departing_from":
        question = ask_departing_from()

    elif topic == "departing_to":
        question = ask_departing_to()

    elif topic == "departure_condition":
        question = ask_departure_condition()

    elif topic == "departure_date":
        question = ask_departure_date()

    elif topic == "departure_time":
        question = ask_departure_time()

    elif topic == "num_adults":
        question = ask_num_adults()

    elif topic == "num_children":
        question = ask_num_children()

    elif topic == "returning":
        question = ask_returning()

    elif topic == 'return_condition':
        question = ask_departure_condition()

    elif topic == "return_date":
        question = ask_return_date()

    elif topic == "return_time":
        question = ask_return_time()

    elif topic == "travelling_alone":
        question = ask_travelling_alone()

    return question
