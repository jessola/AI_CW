from durable.lang import *

from questions import ask_question

def init_questions_answered():
  """Initialises the questions answered knowledge base + rules engine
  """

  with ruleset('questions_answered'):
    @when_all(m.type == 'departing_from')
    def departed_from(c):
      print(ask_question(c.m.type))

    @when_all(+m.type)
    def nothing(c):
      pass