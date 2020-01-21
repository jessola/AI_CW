from experta import *

from questions import ask_question
from validation import validate, suggest
from railway.station import get_station_by_alias
from NLP.NLP import dateFormat2

from .utilities import return_fact
from .fact_types import *


class TicketQsStateRules:
    """Defines the line of questioning required for the chatbot to acquire the
    remaining info needed to book a ticket.
    """
    # Bot still needs more information before ticket can be found
    @Rule(State(status='QUESTIONING'), Task('TICKET'), ~Fact(subject=W()),
          OR(
              ~DepartingFrom(),
              ~DepartingTo(),
              ~DepartureDate(),
              ~DepartureTime(),
              ~Returning(),
              ~ReturnDate(),
          ))
    def more_info_required(self):
        if self.valid:
            self.valid = False
            self.prompt_message(
                ask_question(self.next_ticket_q(), self.context))

    # Question is answered
    @Rule(
        AS.state << State(status='QUESTIONING'),
        Task('TICKET'),
        AS.f << Fact(subject=MATCH.subject, value=MATCH.val),
    )
    def answered_ticket_question(self, state, f, subject, val):
        self.retract(f)

        # When dealing with stations
        try:
            if subject in ['departing_from', 'departing_to']:
                actual_station = get_station_by_alias(val)
                if actual_station:
                    val = actual_station
        except Exception as e:
            self.state_message('I couldn\'t find any stations by that name')

        # When dealing with dates
        try:
            if subject in ['departure_date', 'return_date']:
                actual_date = dateFormat2(val)
        except Exception as e:
            print(str(e))

        # Check for suggestions
        sug = suggest(val, subject, self.context)
        if sug:
            self.just_suggested = True
            self.state_message(sug['message'])
            self.declare(Suggested(subject, sug['value'], sug['original']))
            self.set_prev_state('QUESTIONING')
            self.modify(state, status='SUGGESTING')
            return

        # Check for errors
        error = validate(val, subject, self.context)
        if error:
            self.state_message(error)
            return

        new_fact = return_fact(subject, val)
        self.declare(new_fact)
        self.mark_answered_ticket(subject)

        # When it's a single ticket
        if new_fact[0] == False:
            self.declare(ReturnDate(None), ReturnTime(None))
            self.mark_answered_ticket('return_date', 'return_time')
