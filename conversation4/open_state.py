from experta import *

from .fact_types import State, Task
from questions import ask_question


class OpenStateRules:
    """Defines how interactions with the chatbot work when it does not know what
  task it is doing, for example.
  """
    # Initial State
    @Rule(State(status='OPEN'), ~Task())
    def how_can_bot_help(self):
        self.prompt_message('How can I help you?')

    # Finding Ticket - No details yet
    @Rule(AS.f << State(status='OPEN'), Task('TICKET'))
    def finding_ticket(self, f):
        # self.prompt_message(ask_question('departing_from') + '\n')
        self.modify(f, status='QUESTIONING')
        # print(self.facts[0])

    # Predicting Delays
    @Rule(AS.f << State(status='OPEN'), Task('DELAY'))
    def predicting_delay(self, f):
        # self.state_message('Can\'t do this yet.')
        self.modify(f, status='QUESTIONING')
