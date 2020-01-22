from experta import *
from datetime import datetime
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

delay_freeform_topics = [
    'starting',
    'destination',
    'departure_date',
    'departure_time',
    'previous_delay',
]


class FreeformStateRules:
    """Handles scenarios in which complex input is being provided by the user.
  """

    # Check for suggestions
    def make_multi_suggestions(self, state, params):
        try:
            for topic in freeform_topics:
                if len(params[topic].strip()) > 0 and topic in params.keys():
                    sug = suggest(params[topic], topic, self.context)
                    if sug and not self.just_suggested:
                        self.just_suggested = True
                        self.state_message(sug['message'])
                        self.declare(
                            Suggested(
                                'subject',
                                sug['value'],
                                sug['original'] or None,
                            ))
                        return True

            return False
        except Exception as e:
            print(str(e))

    # Check for errors
    def check_multi_errors(self, params, errors):
        error = None

        for topic in freeform_topics:
            if len(params[topic].strip()) > 0 and topic in params.keys():
                error = validate(params[topic], topic, self.context)

            if error:
                errors.append(topic)

    # Handles the dynamic declaration of facts
    def declare_multi_facts(self, params, errors):
        for topic in freeform_topics:
            if len(params[topic].strip()
                   ) > 0 and topic not in errors and topic in params.keys():
                new_fact = return_fact(topic, params[topic])
                self.declare(new_fact)
                self.mark_answered_ticket(topic)

    # Handles the dynamic declaration of multiple delay facts
    def declare_multi_delay_facts(self, params, errors):
        for topic in delay_freeform_topics:
            if ((len(params[topic].strip()) > 0) and topic not in errors
                    and topic in params.keys()):
                new_fact = return_fact(topic, params[topic])
                self.declare(new_fact)
                self.mark_answered_delay(topic)

    # Prepare error message
    def output_error_message(self, params, errors):
        try:
            if len(errors) < 1:
                return None

            message = 'I\'m not too sure '
            problems = []

            # Add each error string
            for topic in freeform_topics:
                if topic in errors and topic in params.keys():
                    if topic in ['departing_from', 'departing_to']:
                        problems.append('where you\'re %s' %
                                        re.sub('_', ' ', topic))

                    if topic == 'departure_date':
                        problems.append('what day you want to leave')

                    if topic == 'departure_time':
                        problems.append('what time you\'re leaving')

            # Add an or between the last two problems
            if len(problems) > 1:
                last_problem = problems.pop()
                problems[-1] = ' or '.join([problems[-1], last_problem])

            if len(problems) > 0:
                message += ', '.join(problems) + '.'

            return message
        except Exception as e:
            print(str(e))

    # Prepare confirmation message
    def output_confirmation(self, params, errors):
        try:
            # Escape condition

            message = 'You\'re saying '
            details = []

            # Check which details have been specified
            dep_from = params['departing_from'] if len(
                params['departing_from'].strip(
                )) > 0 and 'departing_from' not in errors else None
            dep_to = params['departing_to'] if len(
                params['departing_to'].strip(
                )) > 0 and 'departing_to' not in errors else None
            dep_date = params['departure_date'] if len(
                params['departure_date'].strip(
                )) > 0 and 'departure_date' not in errors else None
            dep_time = params['departure_time'] if len(
                params['departure_time'].strip(
                )) > 0 and 'departure_time' not in errors else None
            ret = params['returning'] if len(params['returning'].strip(
            )) > 0 and 'returning' not in errors else None
            ret_date = params['return_date'] if len(
                params['return_date'].strip(
                )) > 0 and 'return_date' not in errors else None
            ret_time = params['return_time'] if len(
                params['return_time'].strip(
                )) > 0 and 'return_time' not in errors else None

            # Escape condition
            if (not dep_from and not dep_to and not dep_date and not dep_time
                    and not ret and not ret_date and not ret_time):
                return None

            # Departing to and from
            if dep_from and dep_to:
                _string = 'go from %s to %s' % (
                    dep_from.title(),
                    dep_to.title(),
                )
                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)
            elif dep_from or dep_to:
                d = dep_from or dep_to

                _string = 'depart from %s' % d.title(
                ) if dep_from else 'go to %s' % d.title()

                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)

            # Departure date and time
            if dep_date and dep_time:
                _string = 'leave at %s on %s' % (
                    datetime.strptime(dep_date, '%d%m%y').strftime('%D'),
                    datetime.strptime(dep_time, '%H%M').strftime('%H:%M'),
                )
                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)
            elif dep_date or dep_time:
                d = dep_date or dep_time

                _string = 'leave on %s' % datetime.strptime(
                    d, '%d%m%y').strftime(
                        '%D'
                    ) if dep_date else 'leave at %s' % datetime.strptime(
                        d, '%H%M').strftime('%H:%M')

                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)

            # Returning
            if ret:
                _string = 'you want a return ticket'

                details.append(_string)

            # Return date and time
            if ret_date and ret_time:
                _string = 'leave at %s on %s' % (
                    datetime.strptime(ret_date, '%d%m%y').strftime('%D'),
                    datetime.strptime(ret_time, '%H%M').strftime('%H:%M'),
                )
                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)
            elif ret_date or ret_time:
                r = ret_date or ret_time

                _string = 'return on %s' % datetime.strptime(
                    r, '%d%m%y').strftime(
                        '%D'
                    ) if ret_date else 'return at %s' % datetime.strptime(
                        r, '%H%M').strftime('%H:%M')

                if len(details) == 0:
                    _string = 'you want to ' + _string

                details.append(_string)

            # Add an or between the last two details
            if len(details) > 1:
                last_detail = details.pop()
                details[-1] = ' and '.join([details[-1], last_detail])

            if len(details) > 0:
                message += ', '.join(details) + '.'

            return message
        except Exception as e:
            print(str(e))

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

        # Check for errors
        self.check_multi_errors(params, errors)
        if len(errors) > 0:
            self.state_message(self.output_error_message(params, errors))

        try:
            self.declare_multi_facts(params, errors)
        except Exception as e:
            self.state_message(str(e))

        self.retract(params)
        output_message = self.output_confirmation(params, errors)

        try:
            if not output_message:
                self.modify(state, status='QUESTIONING')
                return
            # return
            # pass
            # pass
        except Exception as e:
            self.state_message('Something has gone wrong, I\'m afraid')
            self.reset()
            self.restore()
            return

        self.state_message(output_message)
        self.prompt_message('Is this correct?')

        # self.modify(state, status=self.prev_state)

    # Freeform delay
    @Rule(
        AS.state << State(status='FREEFORM'),
        AS.params << FreeformDelay(),
        Task('DELAY'),
    )
    def freeform_delay(self, state, params):
        errors = []

        try:
            self.declare_multi_delay_facts(params, errors)

            self.state_message('I see.')
            self.modify(state, status=self.prev_state)
        except Exception as e:
            self.state_message(str(e))

        self.retract(params)

    @Rule(AS.state << State(), AS.f << Fact(subject='accepted', value=W()))
    def wait_for_confirmation(self, state, f):
        if f['value'] is True:
            self.state_message('Okay, then.')
            self.modify(state, status=self.prev_state)
            self.retract(f)
        else:
            self.modify(state, status='CONFIRMING')
