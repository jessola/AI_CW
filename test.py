from experta import *
from random import choice, shuffle
from datetime import datetime

from questions import ask_question
from scraping import find_cheapest_ticket

class Conversation(KnowledgeEngine):
    current_question = "departing_from"

    remaining_questions = [
        "departing_from",
        "departing_to",
        "travelling_alone",
        "departure_time",
    ]
    shuffle(remaining_questions)

    # General Methods
    @property
    def requires_more_info(self):
        """Returns true if the system requires more info before selecting a
          ticket.
          """

        return len(self.remaining_questions) > 0

    def prompt_user(self):
        """Picks one of the remaining unknowns and asks the user about it.
          """

        if len(self.remaining_questions) < 1:
            return

        self.current_question = self.remaining_questions[0]

        return ask_question(self.current_question)

    def evaluate_response(self, response):
        """Extracts relevant information from user's response to a prompt.
          
          Arguments:
              response {str} -- The text of the response.
          """
      
        # If there's limited information, assume user only answered one thing.
        # Substitute 'True' for the actual condition
        if True:
          if self.current_question == 'departing_from':
                self.declare(Fact(departing_from=response))

          elif self.current_question == 'departing_to':
                self.declare(Fact(departing_to=response))

          elif self.current_question == 'travelling_alone':
                # For testing purposes, this just checks if first letter is 'y'
                travelling_alone = response.lower()[0] == 'y'

                if not travelling_alone:
                    self.remaining_questions.insert(0, 'num_children')
                    self.remaining_questions.insert(0,'num_adults')

                self.declare(Fact(travelling_alone=travelling_alone))
                
          elif self.current_question == 'departure_time':
                # This is a very basic implementation, definitely not final
                dep_time = datetime.strptime('19-'+ response, '%y-%m-%d %H:%M')
                
                self.declare(Fact(departure_time=dep_time))  
                
          elif self.current_question == 'departure_condition':
                self.declare(Fact(departure_condition=response))

          elif self.current_question == 'num_adults':
                self.declare(Fact(num_adults=int(response)))

          elif self.current_question == 'num_children':
                self.declare(Fact(num_children=int(response)))

          self.run()
    
    # 'Departing From' Specified
    @Rule(Fact(departing_from=MATCH.dep_from))
    def departing_from_answered(self, dep_from):
        self.remaining_questions.remove('departing_from')

    # 'Departing To' Specified
    @Rule(Fact(departing_to=MATCH.dep_to))
    def departing_to_answered(self):
        self.remaining_questions.remove('departing_to')
        
    # 'Departure Time' Specified
    @Rule(Fact(departure_time=MATCH.dep_time))
    def departure_time_answered(self, dep_time):
        # Prompt the user to specify whether it's arrive before or depart after
        # self.remaining_questions.insert(0, 'departure_condition')
        
        self.remaining_questions.remove('departure_time')
        
    #  # 'Departure Condition' Specified
    # @Rule(Fact(departure_condition=MATCH.dep_condition))
    # def departure_time_answered(self, dep_condition):
    #     self.remaining_questions.remove('departure_condition')

    # 'Travelling Alone' Specified
    @Rule(Fact(travelling_alone=W()))
    def travelling_alone_true(self):
        self.remaining_questions.remove('travelling_alone')

    # 'Number of Adults' Specified
    @Rule(Fact(num_adults=W()))
    def num_adults_answered(self):
        self.remaining_questions.remove('num_adults')

    # 'Number of Children' Specified
    @Rule(Fact(num_children=W()))
    def num_children_answered(self):
        self.remaining_questions.remove('num_children')
        
    # Ready to find ticket
    @Rule(
        Fact(departing_from=MATCH.dep_from) &
         Fact(departing_to=MATCH.dep_to) &
         Fact(departure_time=MATCH.dep_time)
        #  Fact(departure_condition=MATCH.dep_condition)
    )
    def find_ticket(self, dep_from, dep_to, dep_time):
        print(find_cheapest_ticket(dep_from, dep_to, {'condition': 'dep', 'date':dep_time}))


c = Conversation()
c.reset()
c.run()

while c.requires_more_info:
      response = input(c.prompt_user() + '\n')

      c.evaluate_response(response)

