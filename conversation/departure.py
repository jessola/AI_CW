from experta import *

from railway.station import get_stations


class DepartureRules:
    # 'Departing From' Specified
    @Rule(AS.f << Fact(departing_from=MATCH.dep_from))
    def departing_from_answered(self, f, dep_from):
        if len(get_stations(dep_from)) < 1:
            # temporary validation message
            print("There are no stations called {}".format(dep_from))

            self.retract(f)
        else:
            self.remaining_questions.remove("departing_from")

    # 'Departing To' Specified
    @Rule(AS.f << Fact(departing_to=MATCH.dep_to))
    def departing_to_answered(self, f, dep_to):
        if len(get_stations(dep_to)) < 1:
            # temporary validation message
            print("There are no stations called {}".format(dep_to))

            self.retract(f)
        else:
            self.remaining_questions.remove("departing_to")

    # 'Departure Time' Specified
    @Rule(Fact(departure_time=MATCH.dep_time))
    def departure_time_answered(self, dep_time):
        # Prompt the user to specify whether it's arrive before or depart after
        self.remaining_questions.insert(0, "departure_condition")

        self.remaining_questions.remove("departure_time")

    # 'Departure Condition' Specified
    @Rule(Fact(departure_condition=MATCH.dep_condition))
    def departure_condition_answered(self, dep_condition):
        self.remaining_questions.remove("departure_condition")
