from experta import *
from datetime import datetime

from questions import ask_question
from tickets.scraping import find_cheapest_ticket
from .fact_types import *


class TicketConfRules:
    """When there is sufficient information for finding a ticket.
  """
    def create_date(self, date, time):
        return datetime.strptime(date + time, '%d%m%y%H%M')

    # There is sufficient info
    @Rule(
        AS.state << State(status='QUESTIONING'),
        Task('TICKET'),
        AND(
            DepartingFrom(MATCH.dep_from),
            DepartingTo(MATCH.dep_to),
            DepartureDate(MATCH.dep_date),
            DepartureTime(MATCH.dep_time),
            Returning(MATCH.ret),
            ReturnDate(MATCH.ret_date),
            ReturnTime(MATCH.ret_time),
        ),
        ~Confirmed(),
    )
    def request_confirmation(self, state, dep_from, dep_to, dep_date, dep_time,
                             ret):
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
              Returning(MATCH.ret),
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
        # Output the ticket
        try:
            self.state_message('*TICKET*' + str(
                find_cheapest_ticket(
                    dep_from,
                    dep_to,
                    {
                        'condition': 'dep',
                        'date': self.create_date(dep_date, dep_time)
                    },
                )))
        except:
            self.state_message(
                'Sorry, I couldn\'t find any tickets matching the criteria you specified.'
            )
