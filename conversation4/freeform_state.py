from experta import *

from .fact_types import *
from validation import validate, suggest


class FreeformStateRules:
    """Handles scenarios in which complex input is being provided by the user.
  """
    @Rule(
        AS.state << State(status='FREEFORM'),
        AS.params << FreeformTicket(),
        ~Fact(subject='accepted'),
    )
    def freeform(self, state, params):
        errors = []

        # TODO: Determine ticket or delays
        self.declare(Task('TICKET'))

        # Check for suggestions
        try:
            sug = suggest(params['dep_from'], 'departing_from', self.context)
            if sug and not self.just_suggested:
                self.just_suggested = True
                self.state_message('Do you mean %s?' % sug)
                self.declare(Suggested('subject', sug))
                # self.set_prev_state('FREEFORM')
                self.modify(state, status='SUGGESTING')
                return
        except Exception as e:
            self.state_message(str(e))

        # Check for errors
        error = validate(params['dep_from'], 'departing_from', self.context)
        if error:
            self.state_message(error)
            errors.append('dep_from')

        # self.retract(params)

        sentence = 'You want to '

        # TODO: Create a nicer method for this
        # Set up the message
        str_dep_from = 'go from {}'.format(
            params['dep_from']) if params['dep_from'] != '' else None

        str_dep_to = 'go to {}'.format(
            params['dep_to']) if params['dep_to'] != '' else None

        str_dep_date = 'travel on {}'.format(
            params['dep_date']) if params['dep_date'] != '' else None

        str_dep_time = 'leave at {}'.format(
            params['dep_time']) if params['dep_time'] != '' else None

        # Stitch them together
        segments = []
        if str_dep_from is not None and 'dep_from' not in errors:
            segments.append(str_dep_from)

        if str_dep_to is not None:
            segments.append(str_dep_to)

        if str_dep_date is not None:
            segments.append(str_dep_date)

        if str_dep_time is not None:
            segments.append(str_dep_time)

        last_two_words = segments[-2:] if len(segments) > 1 else []
        segments = ', '.join(segments[0:-2])
        if len(segments.split(', ')) < 2:
            segments += ', '
        last_two_words = ' and '.join(last_two_words)

        sentence += segments + last_two_words + '.'
        # End of message formatting logic

        # self.declare(Task('TICKET'))

        if params['dep_from'] != '' and 'dep_from' not in errors:
            self.declare(DepartingFrom(params['dep_from']))
            self.mark_answered_ticket('departing_from')

        if params['dep_to'] != '':
            self.declare(DepartingTo(params['dep_to']))
            self.mark_answered_ticket('departing_to')

        if params['dep_date'] != '':
            self.declare(DepartureDate(params['dep_date']))
            self.mark_answered_ticket('departure_date')

        if params['dep_time'] != '':
            self.declare(DepartureTime(params['dep_time']))
            self.mark_answered_ticket('departure_time')

        self.retract(params)
        self.state_message(sentence)
        self.prompt_message('Is this correct?')

        # self.modify(state, status=self.prev_state)

    @Rule(AS.state << State(), AS.f << Fact(subject='accepted', value=W()))
    def wait_for_confirmation(self, state, f):
        if f['value'] is True:
            self.state_message('Okay, then.')
            self.modify(state, status=self.prev_state)
            self.retract(f)
        else:
            self.modify(state, status='CONFIRMING')
