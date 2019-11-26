from .ask_departing_from import ask_departing_from
from .ask_departure_time import ask_departure_time
from .ask_departing_to import ask_departing_to
from .ask_num_adults import ask_num_adults
from .ask_num_children import ask_num_children
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

    elif topic == "departure_time":
        question = ask_departure_time()

    elif topic == "num_adults":
        question = ask_num_adults()

    elif topic == "num_children":
        question = ask_num_children()

    elif topic == "travelling_alone":
        question = ask_travelling_alone()

    return question

