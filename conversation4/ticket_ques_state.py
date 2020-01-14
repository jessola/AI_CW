from experta import *

from questions import ask_question
from validation import validate

from .utilities import return_fact
from .fact_types import *


class TicketQsStateRules:
    """Defines the line of questioning required for the chatbot to acquire the
    remaining info needed to book a ticket.
    """
    # Bot still needs more information before ticket can be found
    @Rule(State(status='QUESTIONING'), Task('TICKET'), ~Fact(subject=W()),
          OR(
              ~DepartingFrom(),
              ~DepartingTo(),
              ~DepartureDate(),
              ~DepartureTime(),
              ~Returning(),
              ~ReturnDate(),
          ))
    def more_info_required(self):
        if self.valid:
            self.valid = False
            self.prompt_message(ask_question(self.next_ticket_q()))

    # Question is answered
    @Rule(
        State(status='QUESTIONING'),
        Task('TICKET'),
        AS.f << Fact(subject=MATCH.subject, value=MATCH.val),
    )
    def answered_ticket_question(self, f, subject, val):
        self.retract(f)

        # Validate
        error = validate(val, subject)
        if error:
            self.state_message(error)
            return

        new_fact = return_fact(subject, val)
        self.declare(new_fact)
        self.mark_answered_ticket(subject)
