from conversation import Conversation

if __name__ == "__main__":
    c = Conversation()
    c.reset()
    c.run()

    while c.requires_more_info:
        response = input(c.prompt_user() + "\n")

        c.evaluate_response(response)

