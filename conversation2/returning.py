from experta import *

from .facts import Question, Confirmed, ReturnTime, Returning, Input


class ReturningRules:
    # User has NOT said if they're returning
    @Rule(Question('returning') & ~Returning())
    def ask_returning(self):
        self.output_question('BOT:\tReturning?\n')

    # Evaluate the user's response to whether or not they're returning
    @Rule(Question('returning') & AS._input << Input())
    def returning_answered(self, _input):
        self.retract(_input)

        # Implement smarted logic for yes or no
        if _input[0].lower()[0] == 'y':
            self.declare(Returning(True))
        elif _input[0].lower()[0] == 'n':
            self.declare(Returning(False))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")

    # Not Returning
    @Rule(AS.f << Question('returning') & Returning(False))
    def not_returning(self, f):
        self.retract(f)

        self.output_statement("BOT:\tOkay, that's fine.")

    # Returning
    @Rule(AS.f << Question('returning') & Returning(True))
    def returning(self, f):
        self.retract(f)

        self.declare(Question('return_time'))

    # No return date specified
    @Rule(Question('return_time') & ~Fact(return_date=W()))
    def ask_return_date(self):
        self.output_question('BOT:\tReturn Date?\n')

    # Return date, i.e. not the time has been specified
    @Rule(
        Question('return_time') & ~Fact(return_date=W())
        & AS._input << Input())
    def return_date_answered(self, _input):
        self.retract(_input)
        self.declare(Fact(return_date=_input[0]))

    # No return time specified
    @Rule(
        Question('return_time') & Fact(return_date=MATCH.ret_date)
        & ~Fact(return_time=W()) & ~Confirmed())
    def ask_return_time(self, ret_date):
        self.output_question(
            'BOT:\tWhen on {} do you want to return?\n'.format(ret_date))

    # Return time specified
    @Rule(
        Question('return_time') & Fact(return_date=MATCH.ret_date)
        & ~Fact(return_time=W()) & AS._input << Input())
    def return_time_answered(self, ret_date, _input):
        self.retract(_input)
        self.declare(Fact(return_time=_input[0]))

    # Date and Time both specified
    @Rule(
        Question('return_time') & Fact(return_date=MATCH.ret_date)
        & Fact(return_time=MATCH.ret_time) & ~Confirmed())
    def ret_date_time_unconfirmed(self, ret_date, ret_time):
        self.output_statement(
            'BOT:\tSo you want to return at {} on {}?'.format(
                ret_time, ret_date))

        self.output_question('BOT:\tIs this right?\n')

    # Await confirmation
    @Rule(
        Question('return_time') & Fact(return_date=MATCH.ret_date)
        & Fact(return_time=MATCH.ret_time) & AS._input << Input())
    def ret_date_time_confirmed(self, ret_date, ret_time, _input):
        self.retract(_input)
        print('HERE')

        # Implement smarted logic for yes or no
        if _input[0].lower()[0] == 'y':
            self.declare(Confirmed(True))
        elif _input[0].lower()[0] == 'n':
            self.declare(Confirmed(False))
        else:
            self.output_statement("BOT:\tI'm not sure what you mean by that.")

    # Return date/time accepted
    @Rule(AS.f << Question('return_time')
          & Fact(return_date=MATCH.ret_date)
          & Fact(return_time=MATCH.ret_time) & AS.f1 << Confirmed(True))
    def ret_date_time_accepted(self, ret_date, ret_time, f, f1):
        self.retract(f)
        self.retract(f1)

        self.output_statement("BOT:\tOkay, I'm aware of your return time.")
        self.declare(ReturnTime(date=ret_date, time=ret_time))

    # Return date/time rejected
    @Rule(
        Question('return_time')
        & AS.f << Fact(return_date=W())
        & AS.f1 << Fact(return_time=W()) & AS.f2 << Confirmed(False))
    def ret_date_time_rejected(self, f, f1, f2):
        self.retract(f)
        self.retract(f1)
        self.retract(f2)

        self.output_statement('Alright, then.')
