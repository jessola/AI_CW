from conversation2 import Engine


if __name__ == "__main__":
    # To start the conversation, type 'ticket' at the first prompt
    e = Engine()
    e.reset()
    e.init_output_statement(lambda x: print(x))
    e.init_output_question(lambda x: e.listen(input(x)))
    e.run()
