from experta import *


class ReturningRules:
    # 'returning' Specified
    @Rule(Fact(returning=W()))
    def returning_answered(self):
        self.remaining_questions.remove("returning")
