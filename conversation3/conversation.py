from durable.lang import *


def init_conversation(statement, question, set_state):
    with statechart('conversation'):
        # Initial state
        with state('start'):

            @to('ticket')
            @when_all(m.subject == 'ticket')
            def ticket(c):
                statement('I can help you find a ticket')

            @to('delay')
            @when_all(m.subject == 'delay')
            def delay(c):
                statement('I can help you predict delays')

        # Find cheapest ticket
        with state('ticket'):
            pass

        # Predict delay
        with state('delay'):
            pass

        # End
        # state('end')


# if __name__ == '__main__':
#     init_conversation(lambda x: print(x), None)
#     assert_fact('conversation', {'subject': 'delay'})
