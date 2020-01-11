from durable.lang import assert_fact, post

from .conversation import init_conversation


class ChatBot:
    """Controls the conversation, either for the process of finding the cheapest 
train ticket from one station to another, or for predicting the delay for a 
particular journey.
"""
    def __init__(self, statement=None, question=None):
        self.statement_output = lambda message: print(message)
        self.question_output = lambda message: self.listen(input(message))
        self.current_state = 'conversation'

        init_conversation(
            self.statement_output,
            self.question_output,
            self.set_state,
        )

    def init_statement_output(self, output):
        """Specifies how statements are conveyed, e.g. by printing to the console.
  
  Arguments:
      output {function} -- Callback function that accepts a string of text.
  """
        self.statement_output = output

    def init_question_output(self, output):
        """Specifies how questions are conveyed, e.g. by printing to the console.
  
  Arguments:
      output {function} -- Callback function that accepts a string of text.
  """
        self.question_output = output

    # The bot says something.
    def output_statement(self, text):
        self.statement_output(text)

    # The bot says something and passes control of conversation to user.
    def output_question(self, text):
        self.question_output(text)

    # The bot 'listens' to what the user inputs.
    def listen(self, message):
        # Extract meaning from the message
        post(self.current_state, {'subject': message})

    # Sets the state of the chatbot, determining the type of questions to ask,
    def set_state(self, state):
        self.current_state = state

    # Start the chatbot.
    def run(self):
        self.output_question('How can I help you?')


if __name__ == '__main__':
    cb = ChatBot()
    cb.run()
