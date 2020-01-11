from durable.lang import *

from .ticket import create_ruleset

questions = [
    'dep_from',
    'dep_to',
    'dep_date',
    'dep_time',
]


class Bot:
    def __init__(self, statement=None, question=None):
        self.unanswered = [*questions]
        self.error = []
        self.unconfirmed = []
        self.confirmed = []

        if statement:
            self.statement_output = statement
        else:
            self.statement_output = lambda message: print(message)

        if question:
            self.question_output = question
        else:
            self.question_output = lambda message: self.listen(input(message))

        create_ruleset(
            self.next_unanswered,
            self.statement_output,
            self.question_output,
            self.mark_confirmed,
            self.mark_unconfirmed,
            self.mark_error,
        )

    @property
    def has_unanswered(self):
        return len(self.unanswered) > 0

    @property
    def has_error(self):
        return len(self.error) > 0

    @property
    def has_unconfirmed(self):
        return len(self.unconfirmed) > 0

    @property
    def has_confirmed(self):
        return len(self.confirmed) > 0

    def output_statement(self, text):
        self.statement_output(text)

    def output_question(self, text):
        self.question_output(text)

    def next_unanswered(self):
        return self.unanswered[0] if self.has_unanswered else None

    @property
    def next_error(self):
        return self.error[0] if self.has_error else None

    def run(self):
        # while self.has_unanswered:
        #     q = self.next_unanswered()
        #     self.output_question(q + '\n')
        #     self.mark_confirmed(q)
        # assert_fact('ticket', {'unanswered': 'dep_from'})
        # assert_fact('ticket', {'unanswered': 'dep_to'})
        # assert_fact('ticket', {'unanswered': 'dep_date'})
        # assert_fact('ticket', {'unanswered': 'dep_time'})
        # assert_fact('ticket', {'dep_from': 'Norwich'})
        # assert_fact('ticket', {'dep_to': 'Cambridge'})
        # assert_fact('ticket', {'dep_date': 'New Years Day'})
        # assert_fact('ticket', {'dep_time': 'noon'})
        # update_state('ticket', {'status': 'start'})
        post('ticket', {'start': True})

    def listen(self, message):
        # TODO: Extract relevant info from text
        if self.next_unanswered():
            post('ticket', {
                'subject': self.next_unanswered(),
                'value': message
            })

    # post('ticket', {'start': True})
    # update_state('ticket', {'status': 'start'})

    def __remove_topic(self, topic):
        if topic in self.unanswered:
            self.unanswered.remove(topic)
        if topic in self.error:
            self.error.remove(topic)
        if topic in self.unconfirmed:
            self.unconfirmed.remove(topic)
        if topic in self.confirmed:
            self.confirmed.remove(topic)

    def mark_unanswered(self, topic):
        self.__remove_topic(topic)
        self.unanswered.append(topic)

    def mark_error(self, topic):
        self.__remove_topic(topic)
        self.error.append(topic)

    def mark_unconfirmed(self, topic):
        self.__remove_topic(topic)
        self.unconfirmed.append(topic)

    def mark_confirmed(self, topic):
        self.__remove_topic(topic)
        self.confirmed.append(topic)


if __name__ == '__main__':
    b = Bot()
    b.run()
    # b.output_question('What is the meaning of life?\n')
