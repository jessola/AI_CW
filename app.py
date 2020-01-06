from conversation2 import Engine
from journeys import get_journeys, get_all_journeys, at_station

if __name__ == "__main__":
    # To start the conversation, type 'ticket' at the first prompt
    # e = Engine()
    # e.reset()
    # e.init_output_statement(lambda x: print(x))
    # e.init_output_question(lambda x: e.listen(input(x)))
    # e.run()

    # for journey in list(get_journeys(lambda j: j['date'].year == 2019)):
    #     if (journey['act_d'] is not None and journey['pla_d'] is not None
    #             and journey['act_a'] is not None
    #             and journey['pla_a'] is not None):
    #         print('Arrival Delay',
    #               int(journey['act_a']) - int(journey['pla_a']),
    #               'Departure Delay',
    #               int(journey['act_d']) - int(journey['pla_d']))
    at_station('DISS')
