from experta import *
from datetime import datetime
import re

from questions import ask_question
from validation import validate, valid_delay_stations as vds

from .utilities import return_fact
from .fact_types import *
from prediction.constants import make_prediction


class DelayConfRules:
    """When there is sufficient information based on which to predict delays.
  """

    # There is sufficient information
    @Rule(
        AS.state << State(status='QUESTIONING'),
        Task('DELAY'),
        AND(
            DepartingFrom(MATCH.start),
            DepartingTo(MATCH.dest),
            OtherStations(MATCH.other),
            #   DepartureDate(MATCH.dep_date),
            #   DepartureTime(MATCH.dep_time),
            PreviousDelay(MATCH.prev_delay),
        ))
    def predict_delay(
        self,
        state,
        start,
        dest,
        other,
        prev_delay,
    ):
        try:
            # Travel Date
            # start_date = datetime.strptime(dep_date + dep_time, '%d%m%y%H%M')
            start_date = datetime.now()

            # Get the information about the stations user is going through
            other = re.sub('[^a-zA-Z\s]', '', other)
            other = re.sub('(\s\s+|\sand\s)', ' ', other)

            # TODO: Add some validation
            other_stations = [stop.lower() for stop in other.split(' ')]
            stops = [
                stop for stop in vds if stop.lower() in other_stations
                or stop.lower() in [start.lower(), dest.lower()]
            ]

            pred = make_prediction(start_date, int(prev_delay), *stops)

            pred_dict = {
                'stops':
                pred,
                'message':
                'You should reach {} at {}, {} minutes later than originally scheduled.'
                .format(
                    dest.title(),
                    pred[-1]['act_a'],
                    pred[-1]['del'],
                )
            }
            pred_str = str(pred_dict).replace("'", '"')

            self.state_message(pred_str)

            self.reset()
            self.restore()
            self.prompt_message('Can I help you with anything else?')
        except Exception as e:
            print(str(e))
            self.state_message(
                'I\'m so sorry, but something seems to have gone wrong.')
            # self.retract([
            #     f for f in self.facts.values() if isinstance(f, OtherStations)
            # ][0])
            # self.delay_questions.insert(0, 'other_stations')
            self.reset()
            self.restore()
            self.prompt_message('Can I help you with anything else?')
