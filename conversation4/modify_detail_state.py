from experta import *

from questions import ask_question
from .fact_types import *
from .utilities import return_fact


class ModStateRules:
    # Method to conveniently retract necessary facts
    def remove_instances(self, subclass):
        to_delete = []

        for fact in self.facts.values():
            if isinstance(fact, type(return_fact(subclass))):
                to_delete.append(fact)

        for fact in to_delete:
            self.retract(fact)

        self.ticket_questions.insert(0, subclass)

    # Modify the current details
    @Rule(
        AS.state << State(status='MODIFYING'),
        Task('TICKET'),
        AS.mod << ToModify(),
    )
    def restore_prev_state(self, state, mod):
        if mod['dep_from']:
            self.remove_instances('departing_from')

        if mod['dep_to']:
            self.remove_instances('departing_to')

        if mod['dep_date']:
            self.remove_instances('departure_date')

        if mod['dep_time']:
            self.remove_instances('departure_time')

        self.modify(state, status='QUESTIONING')
