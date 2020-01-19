from experta import *

from questions import ask_question
from validation import validate, suggest

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
            self.prompt_message(
                ask_question(self.next_ticket_q(), self.context))

    # Question is answered
    @Rule(
        AS.state << State(status='QUESTIONING'),
        Task('TICKET'),
        AS.f << Fact(subject=MATCH.subject, value=MATCH.val),
    )
    def answered_ticket_question(self, state, f, subject, val):
        self.retract(f)

        # Check for suggestions
        if not self.just_suggested:
            sug = suggest(val, subject, self.context)
            if sug:
                self.just_suggested = True
                self.state_message('Do you mean %s?' % sug)
                self.declare(Suggested(subject, sug))
                self.set_prev_state('QUESTIONING')
                self.modify(state, status='SUGGESTING')
                return

        # Check for errors
        error = validate(val, subject, self.context)
        if error:
            self.state_message(error)
            return

        new_fact = return_fact(subject, val)
        self.declare(new_fact)
        self.mark_answered_ticket(subject)

        # When it's a single ticket
        if new_fact[0] == False:
            self.declare(ReturnDate(None), ReturnTime(None))
            self.mark_answered_ticket('return_date', 'return_time')
