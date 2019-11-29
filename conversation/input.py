from datetime import datetime
from experta import *


def extract_info(text):
    """This is a dummy method
      
      Arguments:
          text {str} -- Returns a dict, to test more complicated convo flows.
      """

    return {
        "departing_from": "Norwich",
        "departing_to": "London Liverpool Street",
        "departure_time": datetime(2019, 12, 1, 11, 30),
        "departure_condition": "dep",
    }


class Input(Fact):
    pass


class InputRules:
    count = 0  # Just for test purposes

    @Rule(AS.f << Input(MATCH.text))
    def input(self, f, text):
        self.retract(f)

        self.count += 1  # Just for test purposes

        # Extract relevant information from text using NLP
        details = extract_info(text) if self.count == 1 else {}

        # If there's limited information, assume user only answered one thing.
        if len(details.keys()) < 1:
            if self.current_question == "departing_from":
                self.declare(Fact(departing_from=text))

            elif self.current_question == "departing_to":
                self.declare(Fact(departing_to=text))

            elif self.current_question == "travelling_alone":
                # For testing purposes, this just checks if first letter is 'y'
                travelling_alone = text.lower()[0] == "y"

                if not travelling_alone:
                    self.remaining_questions.insert(0, "num_children")
                    self.remaining_questions.insert(0, "num_adults")

                self.declare(Fact(travelling_alone=travelling_alone))

            elif self.current_question == "returning":
                # For testing purposes, this just checks if first letter is 'y'
                returning = text.lower()[0] == "y"

                self.declare(Fact(returning=returning))

            elif self.current_question == "return_time":
                # This is a very basic implementation, definitely not final
                ret_time = datetime.strptime("19-" + text, "%y-%m-%d %H:%M")

                self.declare(Fact(return_time=ret_time))

            elif self.current_question == "return_condition":
                self.declare(Fact(return_condition=text))

            elif self.current_question == "departure_time":
                # This is a very basic implementation, definitely not final
                dep_time = datetime.strptime("19-" + text, "%y-%m-%d %H:%M")

                self.declare(Fact(departure_time=dep_time))

                self.remaining_questions.insert(0, "departure_condition")

            elif self.current_question == "departure_condition":
                self.declare(Fact(departure_condition=text))

            elif self.current_question == "num_adults":
                self.declare(Fact(num_adults=int(text)))

            elif self.current_question == "num_children":
                self.declare(Fact(num_children=int(text)))
        else:
            if "departing_from" in details.keys():
                self.declare(Fact(departing_from=details["departing_from"]))

            if "departing_to" in details.keys():
                self.declare(Fact(departing_to=details["departing_to"]))

            if "departure_time" in details.keys():
                self.declare(Fact(departure_time=details["departure_time"]))

            if "departure_condition" in details.keys():
                self.declare(Fact(departure_condition=details["departure_condition"]))

