from experta import *

from .fact_types import State, Task, Input
from .utilities import return_fact
from questions import ask_question


class OpenStateRules:
    """Defines how interactions with the chatbot work when it does not know what
  task it is doing, for example.
  """

    # Get all of the currently specified information
    @property
    def context(self):
        current_context = {
            'departing_from': None,
            'departing_to': None,
            'departure_date': None,
            'departure_time': None,
            'returning': None,
        }

        try:
            for key in current_context.keys():
                for fact in self.facts.values():
                    if isinstance(fact, type(return_fact(key))):
                        current_context.update({key: fact[0]})
        except Exception as e:
            print(e)

        return current_context

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

    # # Finish
    # @Rule(AS.f << State(status='OPEN'), ~Task(), AS.text << Input(W()))
    # def end(self, f):
    #     if 'nope' in text[0].lower():
    #         self.state_message('Okay, goodbye!')
    #         self.modify(f, status='END')
