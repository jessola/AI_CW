from experta import *

from questions import ask_question

from .facts import Question, Confirmed, DepartureTime, Input, DepartingFrom


class DepartureTimeRules:
    # No departure date specified
    @Rule(Question('departure_time') & ~Fact(departure_date=W()))
    def ask_departure_date(self):
        self.output_question('BOT:\t{}\n'.format(ask_question('departure_time')))

    # Departure date, i.e. not the time has been specified
    @Rule(
        Question('departure_time') & ~Fact(departure_date=W())
        & AS._input << Input())
    def departure_date_answered(self, _input):
        self.retract(_input)
        self.declare(Fact(departure_date=_input[0]))

    # No departure time specified
    @Rule(
        Question('departure_time') & Fact(departure_date=MATCH.dep_date)
        & ~Fact(departure_time=W()) & ~Confirmed())
    def ask_departure_time(self, dep_date):
        self.output_question(
            'BOT:\tWhen on {} do you want to leave?\n'.format(dep_date))

    # Departure time specified
    @Rule(
        Question('departure_time') & Fact(departure_date=MATCH.dep_date)
        & ~Fact(departure_time=W()) & AS._input << Input())
    def departure_time_answered(self, dep_date, _input):
        self.retract(_input)
        self.declare(Fact(departure_time=_input[0]))

    # Date and Time both specified
    @Rule(
        Question('departure_time') & Fact(departure_date=MATCH.dep_date)
        & Fact(departure_time=MATCH.dep_time) & ~Confirmed())
    def date_time_unconfirmed(self, dep_date, dep_time):
        self.output_statement('BOT:\tSo you want to leave at {} on {}?'.format(
            dep_time, dep_date))

        self.output_question('BOT:\tIs this right?\n')

    # Await confirmation
    @Rule(
        Question('departure_time') & Fact(departure_date=MATCH.dep_date)
        & Fact(departure_time=MATCH.dep_time) & AS._input << Input())
    def date_time_confirmed(self, dep_date, dep_time, _input):
        self.retract(_input)

        # Implement smarted logic for yes or no
        if _input[0].lower()[0] == 'y':
            self.declare(Confirmed(True))
        elif _input[0].lower()[0] == 'n':
            self.declare(Confirmed(False))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")

    # Departure date/time accepted
    @Rule(AS.f << Question('departure_time')
          & Fact(departure_date=MATCH.dep_date)
          & Fact(departure_time=MATCH.dep_time) & AS.f1 << Confirmed(True)
          & OR(~DepartingFrom(), DepartingFrom(MATCH.dep_from)))
    def date_time_accepted(self, dep_date, dep_time, f, f1, dep_from=None):
        self.retract(f)
        self.retract(f1)

        # Summarise the info that's known so far
        # Handle this more elegantly later
        if dep_from:
            self.output_statement(
                "BOT:\tOkay, so you want to travel from {} at {} on {}.".
                format(dep_from, dep_time, dep_date))
        else:
            self.output_statement("BOT:\tOkay, I'll make a note of that.")

        self.declare(DepartureTime(date=dep_date, time=dep_time))
        self.declare(Question('departing_to'))

    # Departure date/time rejected
    @Rule(
        Question('departure_time')
        & AS.f << Fact(departure_date=W())
        & AS.f1 << Fact(departure_time=W()) & AS.f2 << Confirmed(False))
    def date_time_rejected(self, f, f1, f2):
        self.retract(f)
        self.retract(f1)
        self.retract(f2)

        self.output_statement('Alright, then.')
