from experta import *
from random import choice, shuffle
from datetime import datetime

from questions import ask_question

from .departure import DepartureRules
from .input import InputRules, Input
from .passengers import PassengerRules
from .returning import ReturningRules
from .ticket import TicketRules


class Conversation(
    TicketRules,
    DepartureRules,
    PassengerRules,
    ReturningRules,
    InputRules,
    KnowledgeEngine,
):
    current_question = "departing_from"

    remaining_questions = [
        "departing_from",
        "departing_to",
        "travelling_alone",
        "departure_time",
        "returning",
    ]
    shuffle(remaining_questions)

    # General Methods
    @property
    def requires_more_info(self):
        """Returns true if the system requires more info before selecting a
          ticket.
          """

        return len(self.remaining_questions) > 0

    def prompt_user(self):
        """Picks one of the remaining unknowns and asks the user about it.
          """

        if len(self.remaining_questions) < 1:
            return

        self.current_question = self.remaining_questions[0]

        return ask_question(self.current_question) or self.current_question

    def evaluate_response(self, response):
        """Extracts relevant information from user's response to a prompt.
          
          Arguments:
              response {str} -- The text of the response.
          """
          
        self.declare(Input(response))

        self.run()

