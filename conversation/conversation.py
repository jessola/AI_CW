from experta import *
from random import choice, shuffle
from datetime import datetime

from questions import ask_question

from .departure import DepartureRules
from .passengers import PassengerRules
from .returning import ReturningRules
from .ticket import TicketRules


class Conversation(
    TicketRules, DepartureRules, PassengerRules, ReturningRules, KnowledgeEngine
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

        # If there's limited information, assume user only answered one thing.
        # Substitute 'True' for the actual condition
        if True:
            if self.current_question == "departing_from":
                self.declare(Fact(departing_from=response))

            elif self.current_question == "departing_to":
                self.declare(Fact(departing_to=response))

            elif self.current_question == "travelling_alone":
                # For testing purposes, this just checks if first letter is 'y'
                travelling_alone = response.lower()[0] == "y"

                if not travelling_alone:
                    self.remaining_questions.insert(0, "num_children")
                    self.remaining_questions.insert(0, "num_adults")

                self.declare(Fact(travelling_alone=travelling_alone))

            elif self.current_question == "returning":
                # For testing purposes, this just checks if first letter is 'y'
                returning = response.lower()[0] == "y"

                self.declare(Fact(returning=returning))

            elif self.current_question == "return_time":
                # This is a very basic implementation, definitely not final
                ret_time = datetime.strptime("19-" + response, "%y-%m-%d %H:%M")

                self.declare(Fact(return_time=ret_time))

            elif self.current_question == "departure_time":
                # This is a very basic implementation, definitely not final
                dep_time = datetime.strptime("19-" + response, "%y-%m-%d %H:%M")

                self.declare(Fact(departure_time=dep_time))

            elif self.current_question == "departure_condition":
                self.declare(Fact(departure_condition=response))

            elif self.current_question == "num_adults":
                self.declare(Fact(num_adults=int(response)))

            elif self.current_question == "num_children":
                self.declare(Fact(num_children=int(response)))

            self.run()

