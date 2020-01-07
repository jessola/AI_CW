from conversation2 import Engine
from journeys import get_journeys, get_all_journeys, at_station

if __name__ == "__main__":
    # To start the conversation, type 'ticket' at the first prompt
    # e = Engine()
    # e.reset()
    # e.init_output_statement(lambda x: print(x))
    # e.init_output_question(lambda x: e.listen(input(x)))
    # e.run()

    at_station('LIVST')
