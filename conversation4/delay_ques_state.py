from experta import *
import re

from questions import ask_question
from validation import validate, suggest

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
        try:
            self.retract(f)

            # Previous delay
            if subject == 'previous_delay':
                val = re.sub('[^0-9]', '', val)

            # Validate
            # Check for suggestions
            sug = suggest(val, subject, self.context)
            if sug:
                self.just_suggested = True
                self.state_message(sug['message'])
                self.declare(Suggested(subject, sug['value'], sug['original']))
                self.set_prev_state('QUESTIONING')
                self.modify(state, status='SUGGESTING')
                return

            error = validate(val, subject)
            if error:
                self.state_message(error)
                return

            new_fact = return_fact(subject, val)
            self.declare(new_fact)
            self.mark_answered_delay(subject)
        except Exception as e:
            self.state_message('Sorry something went wrong.')
