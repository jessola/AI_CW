from experta import *

from .facts import *


class ConfirmationRules:
    # All required information for finding a ticket is there.
    @Rule(
        DepartingFrom(MATCH.dep_from)
        & DepartingTo(MATCH.dep_to)
        & DepartureTime(date=MATCH.date, time=MATCH.time)
        & Returning(MATCH.ret)
        & ~Confirmed())
    def sufficient_ticket_information(self, dep_from, dep_to, date, time, ret):
        self.output_statement('BOT:\tSo if I have this right, you want a {0} ticket from {1} to {2} on {3} at {4}.'
            .format('return' if ret else 'single', dep_from, dep_to, date, time))

        self.output_question('BOT:\tIs this the information you want me to find you a ticket with?\n')

    # Await confirmation
    @Rule(
        ~Question('incorrect_info')
        & DepartingFrom(MATCH.dep_from)
        & DepartingTo(MATCH.dep_to)
        & DepartureTime(date=MATCH.date, time=MATCH.time)
        & Returning(MATCH.ret)
        & AS._input << Input())
    def ticket_information_unconfirmed(self, dep_from, dep_to, date, time, ret, _input):
        self.retract(_input)

        # Implement smarter logic for yes or no
        if _input[0].lower()[0] == 'y':
            self.declare(Confirmed(True))
        elif _input[0].lower()[0] == 'n':
            self.declare(Confirmed(False))
            self.declare(Question('incorrect_info'))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")


    # Ticket info accepted is handled in .ticket.py

    # Ticket info rejected
    @Rule(
        Question('incorrect_info')
        & DepartingFrom(MATCH.dep_from)
        & DepartingTo(MATCH.dep_to)
        & DepartureTime(date=MATCH.date, time=MATCH.time)
        & Returning(MATCH.ret)
        & AS.f << Confirmed(False))
    def ticket_info_rejected(self, f):
        self.retract(f)

        # self.declare(Question('incorrect_info'))
        self.output_question('BOT:\tOh, which parts are incorrect?\n')

    # User has answered which pieces of information were incorrect
    @Rule(AS.f << Question('incorrect_info') & AS._input << Input())
    def answered_incorrect_info(self, f, _input):
        # Placeholder
        self.output_statement('BOT:\tYou typed "{}"'.format(_input[0]))


