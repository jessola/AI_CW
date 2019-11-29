from experta import *

from questions import ask_question
from railway.station import get_stations

from .facts import Confirmed, Question, DepartingTo, Input


class DepartingToRules:
    # Departing to has NOT been specified
    @Rule(Question("departing_to") & ~DepartingTo())
    def ask_departing_to(self):
        self.output_question("BOT:\t{}\n".format(ask_question("departing_to")))

    # Listen to departure
    @Rule(Question("departing_to") & AS._input << Input())
    def departing_to_answered(self, _input):
        self.retract(_input)
        self.declare(DepartingTo(_input[0]))

    # Departing to specified but not confirmed
    @Rule(
        Question("departing_to") & AS.f << DepartingTo(MATCH.dep_to)
        & ~Confirmed())
    def departing_to_unconfirmed(self, f, dep_to):
        stations = get_stations(dep_to)

        if len(stations) < 1:
            self.output_statement(
                'BOT:\t"{}" is not a station.'.format(dep_to))

            self.retract(f)
        elif len(stations) > 1:
            # List all of the stations they could have meant
            self.output_statement(
                'BOT:\tWhen you say "{}", you could mean:\n {}.'.format(
                    dep_to, '\n'.join([
                        station.name + ' ' + station.code
                        for station in stations
                    ])))

            self.retract(f)
        else:
            self.output_statement(
                "BOT:\tSo you want to go to {}.".format(dep_to))

            self.output_question("BOT:\tIs this correct?\n")

    # Departing to either confirmed or rejected
    @Rule(
        Question("departing_to") & DepartingTo(MATCH.dep_to)
        & AS._input << Input())
    def departing_to_confirmed(self, dep_to, _input):
        self.retract(_input)

        # Implement smarted logic for yes or no
        if _input[0].lower()[0] == "y":
            self.declare(Confirmed(True))
        elif _input[0].lower()[0] == "n":
            self.declare(Confirmed(False))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")

    # Departing to accepted
    @Rule(AS.f << Question("departing_to")
          & AS.f1 << DepartingTo(MATCH.dep_to)
          & AS.f2 << Confirmed(True))
    def departing_to_accepted(self, f, f1, f2, dep_to):
        self.retract(f)
        # self.retract(f1)
        self.retract(f2)

        self.output_statement("BOT:\tOkay, {} it is.".format(dep_to))
        self.declare(Question("returning"))

    # Departing to rejected
    @Rule(
        Question("departing_to") & AS.f << DepartingTo(W())
        & AS.f1 << Confirmed(False))
    def departing_to_rejected(self, f, f1):
        self.retract(f)
        self.retract(f1)

        self.output_statement("BOT:\tOkay, noted.")
