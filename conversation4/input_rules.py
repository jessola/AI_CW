from experta import *

from .fact_types import *


class InputRules:
    """Dealing with user input, including setting the appropriate state based
    on the users interactions with the bot. This may involve switching to an
    error handling state, or a state that accepts multiple details at once
    """
    @Rule(AS.f << Input())
    def retract_input(self, f):
        self.retract(f)
        # print('RETRACTING')

    # Initialise task
    @Rule(AS.text << Input(W()), State(status=W()), ~Task())
    def initialise_task(self, text):
        # TODO: Some extraction and validation
        self.declare(Fact(subject='task', value=text[0].lower()))
        self.retract_input(text)

    # Ticket

    # Check for free form input
    @Rule(AS.text << Input(), AS.state << State(), ~Task('DELAY'), salience=1)
    def check_for_freefrom(self, text, state):
        # TODO: Logic for determining freeform input
        details = text[0].split(', ')
        params = {
            'dep_from': None,
            'dep_to': None,
            'dep_date': None,
            'dep_time': None
        }

        if len(details) > 1:
            for i, detail in enumerate(details):
                try:
                    if detail.strip() != '0':
                        params.update({list(params.keys())[i]: detail})
                except:
                    continue

            self.declare(
                FreeformTicket(
                    dep_from=params['dep_from'] or '',
                    dep_to=params['dep_to'] or '',
                    dep_date=params['dep_date'] or '',
                    dep_time=params['dep_time'] or '',
                ))

            self.retract_input(text)
            self.set_prev_state(state['status'])
            self.modify(state, status='FREEFORM')

    @Rule(
        AS.text << Input(W()),
        AS.state << State(status=W()),
        Task('TICKET'),
    )
    def ticket_input(self, text, state):
        # TODO: Some validation
        if state['status'] == 'QUESTIONING':
            self.declare(Fact(subject=self.next_ticket_q(), value=text[0]))

        if state['status'] == 'CONFIRMING':
            # TODO: Proper 'YES' or 'NO' detection
            res = True if text[0][0].lower() == 'y' else False
            self.declare(Fact(subject='accepted', value=res))

        if state['status'] == 'MODIFYING':
            # TODO: NLP to detect which parts to modify
            res = text[0].lower()

            b_dep_from = 'dep_from' in res
            b_dep_to = 'dep_to' in res
            b_dep_date = 'dep_date' in res
            b_dep_time = 'dep_time' in res

            self.declare(
                ToModify(
                    dep_from=b_dep_from,
                    dep_to=b_dep_to,
                    dep_date=b_dep_date,
                    dep_time=b_dep_time,
                ))

        if state['status'] == 'FREEFORM':
            # TODO: Proper 'YES' or 'NO' detection
            res = True if text[0][0].lower() == 'y' else False
            self.declare(Fact(subject='accepted', value=res))

        self.retract_input(text)

    # Delay
    @Rule(
        AS.text << Input(W()),
        AS.state << State(status=W()),
        Task('DELAY'),
    )
    def delay_input(self, text, state):
        # TODO: Some validation
        if state['status'] == 'QUESTIONING':
            self.declare(Fact(subject=self.next_delay_q(), value=text[0]))

    # Set task to ticket
    @Rule(~Task() & AS.f << Fact(subject='task', value='ticket'), salience=1)
    def task_is_ticket(self, f):
        self.retract(f)
        self.state_message('I can help you find a ticket.')
        self.declare(Task('TICKET'))

    # Set task to delay prediction
    @Rule(~Task() & AS.f << Fact(subject='task', value='delay'))
    def task_is_delay(self, f):
        self.retract(f)
        self.state_message('I\'ll help you deal with delays.')
        self.declare(Task('DELAY'))