from experta import *

from .facts import *
from .confirmation import ConfirmationRules
from .departing_from import DepartingFromRules
from .departing_to import DepartingToRules
from .departure_time import DepartureTimeRules
from .ticket import TicketRules
from .returning import ReturningRules


class Engine(TicketRules, ConfirmationRules, DepartingFromRules,
             DepartingToRules, DepartureTimeRules, ReturningRules,
             KnowledgeEngine):

    # Sets the stream of output for statements
    def init_output_statement(self, CB=None):
        if CB:
            self.output_statement = CB

    # Sets the stream of output for questions
    def init_output_question(self, CB=None):
        if CB:
            self.output_question = CB

    # What the user says to the system
    def listen(self, text):
        self.declare(Input(text))

    # Initial facts
    @DefFacts()
    def start_engine(self):
        yield Started(True)
        yield Topic('start')
        # yield Returning(False)
        # yield DepartingFrom('Norwich')
        # yield Fact(departure_date="12/12")
        # yield Fact(departure_time="9:30")
        # yield DepartingTo('London Liverpool Street')

    # Starts up the chatbot
    @Rule(Started(True))
    def engine_started(self):
        self.output_statement("BOT:\tHello, I'm a bot.")
        self.output_question('BOT:\tHow can I help you?\n')

    # Determines which task the chatbot is doing
    @Rule(AS._input << Input() & AS.f << Topic('start'))
    def topic_answered(self, f, _input):
        self.retract(_input)

        # Implement smarter logic to see what the user wants
        if _input[0].lower() == 'delays':
            self.declare(Task('delays'))
            self.retract(f)
        elif _input[0].lower() == 'ticket':
            self.declare(Task('ticket'))
            self.retract(f)
        else:
            self.output_statement("BOT:\tI'm not sure what you mean.")
            self.output_question("BOT:\tHow can I help you?\n")

    # Start finding the cheapest ticket
    @Rule(Task('ticket'))
    def task_ticket(self):
        self.output_statement('BOT:\tSure, I can help you find a ticket')

        self.declare(Question('departing_from'))

    # Start sorting delays
    @Rule(Task('delays'))
    def task_delays(self):
        self.output_statement('BOT:\tI can not yet predict delays. Sorry.')


if __name__ == '__main__':
    e = Engine()
    e.reset()
    e.init_output_statement(lambda x: print(x))
    e.init_output_question(lambda x: e.listen(input(x)))
    e.run()