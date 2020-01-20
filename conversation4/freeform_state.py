from experta import *
import re

from .fact_types import *
from .utilities import return_fact
from validation import validate, suggest

freeform_topics = [
    'departing_from',
    'departing_to',
    'departure_date',
    'departure_time',
    'returning',
    'return_date',
    'return_time',
]


class FreeformStateRules:
    """Handles scenarios in which complex input is being provided by the user.
  """

    # Check for suggestions
    def make_multi_suggestions(self, state, params):
        try:
            for topic in freeform_topics:
                if len(params[topic].strip()) > 0:
                    sug = suggest(params[topic], topic, self.context)
                    if sug and not self.just_suggested:
                        self.just_suggested = True
                        self.state_message(sug['message'])
                        self.declare(Suggested('subject', sug['value']))
                        return True

            return False
        except Exception as e:
            self.state_message(str(e))

    # Check for errors
    def check_multi_errors(self, params, errors):
        error = None

        for topic in freeform_topics:
            if len(params[topic].strip()) > 0:
                error = validate(params[topic], topic, self.context)

            if error:
                errors.append(topic)

    # Handles the dynamic declaration of facts
    def declare_multi_facts(self, params, errors):
        for topic in freeform_topics:
            if len(params[topic].strip()) > 0 and topic not in errors:
                new_fact = return_fact(topic, params[topic])
                self.declare(new_fact)
                self.mark_answered_ticket(topic)

    # Prepare error message
    def output_error_message(self, params, errors):
        try:
            if len(errors) < 1:
                return None

            message = 'I\'m not too sure '
            problems = []

            # Add each error string
            for topic in freeform_topics:
                if topic in errors:
                    if topic in ['departing_from', 'departing_to']:
                        problems.append('where you\'re %s' %
                                        re.sub('_', ' ', topic))

                    if topic == 'departure_date':
                        problems.append('what day you want to leave')

                    if topic == 'departure_time':
                        problems.append('what time you\'re leaving')

            if len(problems) > 0:
                message += ', '.join(problems) + '.'

            return message
        except Exception as e:
            self.state_message(str(e))

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
        if self.make_multi_suggestions(state, params):
            self.modify(state, status='SUGGESTING')
            return

        # try:
        #     sug = suggest(params['departing_from'], 'departing_from',
        #                   self.context)
        #     if sug and not self.just_suggested:
        #         self.just_suggested = True
        #         self.state_message('Do you mean %s?' % sug)
        #         self.declare(Suggested('subject', sug))
        #         # self.set_prev_state('FREEFORM')
        #         self.modify(state, status='SUGGESTING')
        #         return
        # except Exception as e:
        #     self.state_message(str(e))

        # Check for errors
        self.check_multi_errors(params, errors)
        if len(errors) > 0:
            self.state_message(self.output_error_message(params, errors))
        # error = validate(params['departing_from'], 'departing_from',
        #                  self.context)
        # if error:
        #     self.state_message(error)
        #     errors.append('departing_from')

        # self.retract(params)

        sentence = 'You want to '

        # TODO: Create a nicer method for this
        # Set up the message
        str_departing_from = 'go from {}'.format(
            params['departing_from']
        ) if params[
            'departing_from'] and 'departing_from' not in errors != '' else None

        str_departing_to = 'go to {}'.format(params['departing_to']) if params[
            'departing_to'] != '' and 'departing_to' not in errors else None

        str_departure_date = 'travel on {}'.format(
            params['departure_date']
        ) if params['departure_date'] != '' else None

        str_dep_time = 'leave at {}'.format(
            params['departure_time']
        ) if params['departure_time'] != '' else None

        # Stitch them together
        segments = []
        if str_departing_from is not None and 'departing_from' not in errors:
            segments.append(str_departing_from)

        if str_departing_to is not None:
            segments.append(str_departing_to)

        if str_departure_date is not None:
            segments.append(str_departure_date)

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
        try:
            self.declare_multi_facts(params, errors)
        except Exception as e:
            print(str(e))

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
