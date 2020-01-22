from experta import Fact, Field


# General
class Input(Fact):
    pass


class Task(Fact):
    pass


class State(Fact):
    pass


class DepartingFrom(Fact):
    pass


class DepartingTo(Fact):
    pass


class DepartureDate(Fact):
    pass


class DepartureTime(Fact):
    pass


class Suggested(Fact):
    pass


# Finding Tickets
class Returning(Fact):
    pass


class ReturnDate(Fact):
    pass


class ReturnTime(Fact):
    pass


class Confirmed(Fact):
    pass


class FreeformTicket(Fact):
    departing_from = Field(str, default='')
    departing_to = Field(str, default='')
    departure_date = Field(str, default='')
    departure_time = Field(str, default='')
    returning = Field(str, default='')
    return_date = Field(str, default='')
    return_time = Field(str, default='')


class ToModify(Fact):
    """Fields are set to true if the corresponding detail is to be modified,
    i.e. because the user either changed their mind or wants to correct the bot.  
    """
    dep_from = Field(bool, default=False)
    dep_to = Field(bool, default=False)
    dep_date = Field(bool, default=False)
    dep_time = Field(bool, default=False)
    returning = Field(bool, default=False)
    ret_date = Field(bool, default=False)
    ret_time = Field(bool, default=False)


# Delays
class PreviousDelay(Fact):
    pass


class OtherStations(Fact):
    pass


class FreeformDelay(Fact):
    starting = Field(str, default='')
    destination = Field(str, default='')
    # departure_date = Field(str, default='')
    # departure_time = Field(str, default='')
    previous_delay = Field(str, default='')
