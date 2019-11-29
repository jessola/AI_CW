from experta import *

from questions import ask_question
from railway.station import get_stations

from .facts import Confirmed, Question, DepartingFrom, Input


class DepartingFromRules:
    # Departure has NOT been specified
    @Rule(Question('departing_from') & ~DepartingFrom())
    def ask_departing_from(self):
        self.output_question('BOT:\t{}\n'.format(
            ask_question('departing_from')))

    # Listen to departure
    @Rule(Question('departing_from') & AS._input << Input())
    def departing_from_answered(self, _input):
        self.retract(_input)
        self.declare(DepartingFrom(_input[0]))

    # Departure specified but not confirmed
    @Rule(
        Question('departing_from')
        & AS.f << DepartingFrom(MATCH.dep_from) & ~Confirmed())
    def departing_from_unconfirmed(self, f, dep_from):
        stations = get_stations(dep_from)

        if len(stations) < 1:
            self.output_statement(
                'BOT:\t"{}" is not a station.'.format(dep_from))

            self.retract(f)
        elif len(stations) > 1:
            # List all of the stations they could have meant
            self.output_statement(
                'BOT:\tWhen you say "{}", you could mean:\n {}.'.format(
                    dep_from, '\n'.join([
                        station.name + ' ' + station.code
                        for station in stations
                    ])))

            self.retract(f)
        else:
            self.output_statement(
                'BOT:\tSo you want to leave from {}.'.format(dep_from))

            self.output_question('BOT:\tIs this correct?\n')

    # Departing from either confirmed or rejected
    @Rule(
        Question('departing_from') & DepartingFrom(MATCH.dep_from)
        & AS._input << Input())
    def departing_from_confirmed(self, dep_from, _input):
        self.retract(_input)

        # Implement smarted logic for yes or no
        if _input[0].lower()[0] == 'y':
            self.declare(Confirmed(True))
        elif _input[0].lower()[0] == 'n':
            self.declare(Confirmed(False))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")

    # Departing from accepted
    @Rule(AS.f << Question('departing_from')
          & DepartingFrom(MATCH.dep_from) & AS.f1 << Confirmed(True))
    def departing_from_accepted(self, f, f1, dep_from):
        self.retract(f)
        self.retract(f1)

        self.output_statement('BOT:\tOkay, {} it is.'.format(dep_from))
        self.declare(Question('departure_time'))

    # Departing from rejected
    @Rule(
        Question('departing_from') & AS.f << DepartingFrom(W())
        & AS.f1 << Confirmed(False))
    def departing_from_rejected(self, f, f1):
        self.retract(f)
        self.retract(f1)

        self.output_statement('BOT:\tOkay, noted.')