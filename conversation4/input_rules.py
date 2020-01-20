from experta import *

from .fact_types import *
from NLP.NLP import inputNLP


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
        details2 = inputNLP(text[0])

        params = {
            'dep_from': None,
            'dep_to': None,
            'dep_date': None,
            'dep_time': None,
            'returning': None,
        }

        if details2['departing_from'] or details2['departing_to']:
            dep_from = details2['departing_from'] or None
            dep_to = details2['departing_to'] or None
            # for i, detail in enumerate(details):
            # try:
            #     if detail.strip() != '0':
            #         params.update({list(params.keys())[i]: detail})
            # except:
            #     continue
            if dep_from:
                params['dep_from'] = dep_from

            if dep_to:
                params['dep_to'] = dep_to

            self.declare(
                FreeformTicket(
                    departing_from=params['dep_from'] or '',
                    departing_to=params['dep_to'] or '',
                    departure_date=params['dep_date'] or '',
                    departure_time=params['dep_time'] or '',
                    returning=params['returning'] or '',
                ))

            self.retract_input(text)
            self.set_prev_state(state['status'])
            self.modify(state, status='FREEFORM')

        # if len(details) > 1:
        #     for i, detail in enumerate(details):
        #         try:
        #             if detail.strip() != '0':
        #                 params.update({list(params.keys())[i]: detail})
        #         except:
        #             continue

        #     self.declare(
        #         FreeformTicket(
        #             departing_from=params['dep_from'] or '',
        #             departing_to=params['dep_to'] or '',
        #             departure_date=params['dep_date'] or '',
        #             departure_time=params['dep_time'] or '',
        #             returning=params['returning'] or '',
        #         ))

        #     self.retract_input(text)
        #     self.set_prev_state(state['status'])
        #     self.modify(state, status='FREEFORM')

    # Ticket questioning
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

        if state['status'] == 'SUGGESTING':
            # TODO: Proper 'YES' or 'NO' detection
            res = True if text[0][0].lower() == 'y' else False
            self.declare(Fact(subject='agreed', value=res))

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

    # Set task to ticket or delay
    @Rule(~Task() & AS.f << Fact(subject='task', value=W()), salience=1)
    def task_is_ticket(self, f):
        self.retract(f)
        res = f['value'].lower()

        if 'ticket' in res and not 'delay' in res:
            self.state_message('Sure thing.')
            self.declare(Task('TICKET'))
        elif 'delay' in res and not 'ticket' in res:
            self.state_message(
                'I\'ll try my best to help you with your delay.')
            self.declare(Task('DELAY'))
        else:
            self.state_message('I\'m not too sure what you mean.')
            self.prompt_message(
                'I can help you find the cheapest ticket for your journey or predict the delay for a journey you\'re making. Which will it be?'
            )