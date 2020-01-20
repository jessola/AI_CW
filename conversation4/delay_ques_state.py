from experta import *

from questions import ask_question
from validation import validate

from .utilities import return_fact
from .fact_types import *


class DelayQsStateRules:
    """The delay task has been set
  """
    # More information is required before a delay prediction is made
    @Rule(State(status='QUESTIONING'), Task('DELAY'), ~Fact(subject=W()),
          OR(
              ~DepartingFrom(),
              ~DepartingTo(),
              ~DepartureDate(),
              ~DepartureTime(),
              ~PreviousDelay(),
          ))
    def more_delay_info_required(self):
        if self.valid:
            self.valid = False
            self.prompt_message(
                ask_question(self.next_delay_q(), self.context)
                or self.next_delay_q())

    # Question is answered
    @Rule(
        State(status='QUESTIONING'),
        Task('DELAY'),
        AS.f << Fact(subject=MATCH.subject, value=MATCH.val),
    )
    def answered_delay_question(self, f, subject, val):
        self.retract(f)

        # Validate
        error = validate(val, subject)
        if error:
            self.state_message(error)
            return

        new_fact = return_fact(subject, val)
        self.declare(new_fact)
        self.mark_answered_delay(subject)

        # # When it's a single ticket
        # if new_fact[0] == False:
        #     self.declare(ReturnDate(None), ReturnTime(None))
        #     self.mark_answered_ticket('return_date', 'return_time')
