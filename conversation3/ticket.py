from durable.lang import *

# def add_stuff():
#     @when_all(m.subject == 'test')
#     def test(c):
#         print('This is a test')

#     @when_all((m.subject == 'test'), (m.subject == 'dep_time'))
#     def testdeptime(c):
#         print('Something else can be added here')

# with ruleset('questions'):

#     # From
#     @when_all((m.subject == 'dep_from') & (+m.value))
#     def set_dep_from(c):
#         c.assert_fact({'dep_from': c.m.value})

#     # To
#     @when_all((m.subject == 'dep_to') & (+m.value))
#     def set_dep_to(c):
#         c.assert_fact({'dep_to': c.m.value})

#     # Date - Departure
#     @when_all((m.subject == 'dep_date') & (+m.value))
#     def set_dep_date(c):
#         c.assert_fact({'dep_date': c.m.value})

#     # Time - Departure
#     @when_all((m.subject == 'dep_time') & (+m.value))
#     def set_dep_time(c):
#         c.assert_fact({'dep_time': c.m.value})

#     # Sufficient Information
#     @when_all(
#         c.first << (+m.dep_from) & (m.confirmed == True),
#         c.second << (+m.dep_to) & (m.confirmed == True),
#         c.third << (+m.dep_date) & (m.confirmed == True),
#         c.fourth << (+m.dep_time) & (m.confirmed == True),
#     )
#     def finished(c):
#         print('Travelling from {} to {} on {} at {}.'.format(
#             c.first.dep_from,
#             c.second.dep_to,
#             c.third.dep_date,
#             c.fourth.dep_time,
#         ))

#     add_stuff()

# questions = [
#     'dep_from',
#     'dep_to',
#     'dep_date',
#     'dep_time',
# ]

# b = Bot()


def answer_questions(next_unanswered, statement, question, conf, unc, error):
    @when_all((m.subject == 'dep_from') & +m.value)
    def set_dep_from(c):
        conf(next_unanswered())
        # c.retract_fact({'unanswered': 'dep_from'})
        c.assert_fact({'dep_from': c.m.value})

    @when_all((m.subject == 'dep_to') & +m.value)
    def set_dep_to(c):
        conf(next_unanswered())
        # c.retract_fact({'unanswered': 'dep_to'})
        c.assert_fact({'dep_to': c.m.value})

    @when_all((m.subject == 'dep_date') & +m.value)
    def set_dep_date(c):
        conf(next_unanswered())
        # c.retract_fact({'unanswered': 'dep_date'})
        c.assert_fact({'dep_date': c.m.value})

    @when_all((m.subject == 'dep_time') & +m.value)
    def set_dep_time(c):
        conf(next_unanswered())
        # c.retract_fact({'unanswered': 'dep_time'})
        c.assert_fact({'dep_time': c.m.value})


def create_ruleset(next_unanswered, statement, question, conf, unc, error):
    with ruleset('ticket'):

        @when_all(m.start == True)
        def start(c):
            print('Something')

        answer_questions(
            next_unanswered,
            statement,
            question,
            conf,
            unc,
            error,
        )

        # @when_all(s.status == 'start')
        # def start(c):
        #     c.s.status = 'conversing'

        # There are errors.

        # Confirmation is needed.

        # There are unanswered questions.
        @when_any(
            all(-m.dep_from),
            all(-m.dep_to),
            all(-m.dep_date),
            all(-m.dep_time),
        )
        def unanswered(c):
            if next_unanswered():
                question(next_unanswered() + '\n')

        # @when_all(+m.unanswered)
        # def unanswered(c):
        #     question(next_unanswered() + '\n')

        @when_all(c.first << +m.dep_from, c.second << +m.dep_to,
                  c.third << +m.dep_date, c.fourth << +m.dep_time)
        def sufficient_info(c):
            try:
                statement('Travelling from {} to {} on {} at {}.'.format(
                    c.first.dep_from,
                    c.second.dep_to,
                    c.third.dep_date,
                    c.fourth.dep_time,
                ))
            except Exception as e:
                print('str(e)')
