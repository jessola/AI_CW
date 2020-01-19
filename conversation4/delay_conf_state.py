from experta import *
from datetime import datetime

from questions import ask_question
from validation import validate

from .utilities import return_fact
from .fact_types import *
from prediction.constants import make_prediction


class DelayConfRules:
    """When there is sufficient information based on which to predict delays.
  """

    # There is sufficient information
    @Rule(AS.state << State(status='QUESTIONING'), Task('DELAY'),
          AND(
              DepartingFrom(MATCH.dep_from),
              DepartingTo(MATCH.dep_to),
              DepartureDate(MATCH.dep_date),
              DepartureTime(MATCH.dep_time),
              PreviousDelay(MATCH.prev_delay),
          ))
    def predict_delay(
        self,
        state,
        dep_from,
        dep_to,
        dep_date,
        dep_time,
        prev_delay,
    ):
        start_date = datetime.strptime(dep_date + dep_time, '%d%m%y%H%M')
        pred = make_prediction(
            start_date,
            int(prev_delay),
            'Norwich',
            'Diss',
            'Stowmarket',
            'Ipswich',
            'Manningtree',
            'Colchester',
            'London',
        )

        pred = {
            'stops':
            pred,
            'message':
            'You should reach {} at {}, {} minutes later than originally scheduled.'
            .format(
                dep_to.title(),
                pred[-1]['act_a'],
                pred[-1]['del'],
            )
        }
        pred_str = str(pred).replace("'", '"')

        self.state_message(pred_str)
