# from conversation import Conversation
from conversation2 import Engine


if __name__ == "__main__":
    # c = Conversation()
    # c.reset()
    # c.run()

    # while c.requires_more_info:
    #     response = input(c.prompt_user() + "\n")

    #     c.evaluate_response(response)
    e = Engine()
    e.reset()
    e.init_output_statement(lambda x: print(x))
    e.init_output_question(lambda x: e.listen(input(x)))
    e.run()

