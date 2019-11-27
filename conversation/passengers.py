from experta import *


class PassengerRules:
    # 'Travelling Alone' Specified
    @Rule(Fact(travelling_alone=W()))
    def travelling_alone_true(self):
        self.remaining_questions.remove("travelling_alone")

    # 'Number of Adults' Specified
    @Rule(Fact(num_adults=W()))
    def num_adults_answered(self):
        self.remaining_questions.remove("num_adults")

    # 'Number of Children' Specified
    @Rule(Fact(num_children=W()))
    def num_children_answered(self):
        self.remaining_questions.remove("num_children")
