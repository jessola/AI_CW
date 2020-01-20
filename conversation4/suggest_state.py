from experta import *
from datetime import datetime

from questions import ask_question
from validation import validate

from .utilities import return_fact
from .fact_types import *


class SuggestionStateRules:
    """Controls the logic for the bot suggesting something a correction to the
  user before awaiting a response.
  """
    @Rule(AS.state << State(status='SUGGESTING'), AS.sug << Suggested(),
          AS.f << Fact(subject="agreed", value=W()), ~FreeformTicket())
    def suggest(self, state, sug, f):
        # self.state_message('The suggestion is: %s' % f[0])
        if f['value'] is False:
            self.retract(sug)
            self.retract(f)
            self.modify(state, status=self.prev_state)
        else:
            to_delete = []

            for fact in self.facts.values():
                if isinstance(fact, type(return_fact(sug[0]))):
                    to_delete.append(fact)

            for fact in to_delete:
                self.retract(fact)

            self.declare(Fact(subject=sug[0], value=sug[1]))
            self.retract(sug)
            self.retract(f)
            self.modify(state, status=self.prev_state)

    @Rule(AS.state << State(status='SUGGESTING'), AS.sug << Suggested(),
          AS.f << Fact(subject="agreed", value=W()),
          AS.free << FreeformTicket())
    def suggest_freeform(self, state, sug, f, free):
        if f['value'] is False:
            self.just_suggested = True
            self.retract(sug)
            self.retract(f)
            self.modify(state, status='FREEFORM')

        else:
            to_delete = []

            for fact in self.facts.values():
                if isinstance(fact, type(return_fact(sug[0]))):
                    to_delete.append(fact)

            for fact in to_delete:
                self.retract(fact)
            self.modify(free, departing_from=sug[1])
            self.retract(sug)
            self.retract(f)
            self.modify(state, status='FREEFORM')
