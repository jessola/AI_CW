from experta import Fact, Field


class Started(Fact):
    pass


class Confirmed(Fact):
    pass


class Input(Fact):
    pass


class Topic(Fact):
    pass


class Task(Fact):
    pass


class Question(Fact):
    pass


class DepartingFrom(Fact):
    pass


class DepartingTo(Fact):
    pass


class DepartureTime(Fact):
    date = Field(str, mandatory=True)
    time = Field(str, mandatory=True)


class Returning(Fact):
    pass


class ReturnTime(Fact):
    date = Field(str, mandatory=True)
    time = Field(str, mandatory=True)