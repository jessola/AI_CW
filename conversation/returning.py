from experta import *


class ReturningRules:
    # 'Returning' Specified
    @Rule(Fact(returning=MATCH.returning))
    def returning_answered(self, returning):
        if returning:
            self.remaining_questions.insert(0, "return_time")

        self.remaining_questions.remove("returning")

    # 'Return Time' Specified
    @Rule(Fact(return_time=MATCH.ret_time))
    def return_time_answered(self, ret_time):
        # Prompt the user to specify whether it's arrive before or depart after
        # self.remaining_questions.insert(0, "return_condition")

        self.remaining_questions.remove("return_time")
