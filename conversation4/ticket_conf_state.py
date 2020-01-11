from experta import *

from questions import ask_question
from .fact_types import *


class TicketConfRules:
    """When there is sufficient information for finding a ticket.
  """
    # There is sufficient info
    @Rule(AS.state << State(status='QUESTIONING'), Task('TICKET'),
          AND(
              DepartingFrom(MATCH.dep_from),
              DepartingTo(MATCH.dep_to),
              DepartureDate(MATCH.dep_date),
              DepartureTime(MATCH.dep_time),
          ), ~Confirmed())
    def request_confirmation(self, state, dep_from, dep_to, dep_date,
                             dep_time):
        self.modify(state, status='CONFIRMING')
        self.prompt_message(
            'So you want to travel from %s to %s on %s at %s?' % (
                dep_from,
                dep_to,
                dep_date,
                dep_time,
            ))

    @Rule(AS.state << State(status='CONFIRMING'), Task('TICKET'),
          AS.f << Fact(subject='accepted', value=W()), ~Confirmed())
    def check_for_acceptance(self, state, f):
        self.retract(f)
        if f['value'] == True:
            self.state_message('Okay, great.')
            self.declare(Confirmed(True))
        else:
            self.prompt_message('Which parts are wrong?')
            self.modify(state, status='MODIFYING')

    # There is sufficient info
    @Rule(AS.state << State(status='CONFIRMING'), Task('TICKET'),
          AND(
              DepartingFrom(MATCH.dep_from),
              DepartingTo(MATCH.dep_to),
              DepartureDate(MATCH.dep_date),
              DepartureTime(MATCH.dep_time),
          ), Confirmed())
    def verify_ticket_info(
        self,
        state,
        dep_from,
        dep_to,
        dep_date,
        dep_time,
    ):
        self.state_message('I\'ll find the cheapest ticket for you now.')
