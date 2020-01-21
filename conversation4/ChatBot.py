from experta import *

from .fact_types import Task, State, Input

# Rulesets
from .open_state import OpenStateRules
from .ticket_ques_state import TicketQsStateRules
from .delay_ques_state import DelayQsStateRules
from .ticket_conf_state import TicketConfRules
from .delay_conf_state import DelayConfRules
from .modify_detail_state import ModStateRules
from .freeform_state import FreeformStateRules
from .input_rules import InputRules
from .suggest_state import SuggestionStateRules

questions_ticket = [
    'departing_from',
    'departing_to',
    'departure_date',
    'departure_time',
    'returning',
    'return_date',
    'return_time',
]

questions_delay = [
    'starting',
    'destination',
    'other_stations',
    'departure_date',
    'departure_time',
    'previous_delay',
]


class ChatBot(
        FreeformStateRules,
        InputRules,
        ModStateRules,
        SuggestionStateRules,
        TicketConfRules,
        TicketQsStateRules,
        DelayConfRules,
        DelayQsStateRules,
        OpenStateRules,
        KnowledgeEngine,
):
    def __init__(self, state_message=None, prompt_message=None):
        super().__init__()
        self.valid = False
        self.just_suggested = False
        self.prev_state = None
        self.ticket_questions = [*questions_ticket]
        self.delay_questions = [*questions_delay]
        self.__state_message = state_message or (lambda m: print(m))
        self.__prompt_message = prompt_message or (
            lambda m: self.listen(input(m)))

    @property
    def has_ticket_qs(self):
        return len(self.ticket_questions) > 0

    @property
    def has_delay_qs(self):
        return len(self.delay_questions) > 0

    # Set up initial facts
    @DefFacts()
    def initial_state(self):
        yield State(status='OPEN')

    # Restore the original state
    def restore(self):
        self.ticket_questions = [*questions_ticket]
        self.delay_questions = [*questions_delay]

    # Set the previous state, so bot can resume questioning after freeform input
    def set_prev_state(self, state):
        if state.upper() != 'FREEFORM':
            self.prev_state = state.upper()

    # Accept user input
    def listen(self, message):
        self.valid = True
        self.declare(Input(message))

    # Make the bot say something.
    def state_message(self, message):
        self.__state_message(message)

    # Make the bot say something, before letting the user dictate conversation
    def prompt_message(self, message):
        self.__prompt_message(message)

    # The next question
    def next_ticket_q(self):
        return self.ticket_questions[0] if self.has_ticket_qs else None

    def next_delay_q(self):
        return self.delay_questions[0] if self.has_delay_qs else None

    # Mark a topic as answered, i.e. removing it from the list
    def mark_answered_ticket(self, *topics):
        self.just_suggested = False

        for topic in topics:
            if topic in self.ticket_questions:
                self.ticket_questions.remove(topic)

    def mark_answered_delay(self, *topics):
        self.just_suggested = False

        for topic in topics:
            if topic in self.delay_questions:
                self.delay_questions.remove(topic)


if __name__ == '__main__':
    c = ChatBot()
    c.reset()
    c.run()
    # while c.has_ticket_qs:
    #     print(c.next_ticket_q())
