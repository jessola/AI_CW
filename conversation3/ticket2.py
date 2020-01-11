from durable.lang import *


def is_error(station, ques):
    if station.lower() == 'london' and ques == 'dep_from':
        return 'You cannot go from London'

    if station.lower() == 'norwich' and ques == 'dep_to':
        return 'You cannot go to Norwich'

    return None


ques = ['dep_from', 'dep_to', 'dep_date', 'dep_time']

error = []


def ask_question():
    return ques[0] or None


def ask_error():
    return error[0] or None


with ruleset('conversation'):

    @when_any(all(c.first << (+m.dep_from) & (+m.dep_to)),
              all(c.second << (+m.dep_date) & (+m.dep_time)))
    def answered_multiple(c):
        # print('Going from {} to {}'.format(c.m.dep_from, c.m.dep_to))
        if c.first:
            print('Going from {} to {}'.format(c.first.dep_from,
                                               c.first.dep_to))

        if c.second:
            print('Going on {} at {}'.format(c.second.dep_date,
                                             c.second.dep_time))

    @when_all((+m.subject & +m.value))
    def answered(c):
        if is_error(c.m.value, ques[0]) is not None:
            try:
                print(is_error(c.m.value, ques[0]))
                # c.assert_fact({ques[0]: c.m.value, 'valid': False})
                c.post({'error': ques[0]})
                error.insert(0, ques[0])
            except:
                pass

        else:
            c.assert_fact({ques[0]: c.m.value, 'valid': True})
            if len(ques) > 0:
                c.post({
                    'subject': ques.pop(0),
                    'value': input(ask_question() + '\n')
                })

    @when_all(+m.error)
    def confirm(c):
        if len(error) > 0:
            c.post({'subject': c.m.error, 'value': input(ask_error() + '\n')})

    @when_all(
        c.first << (+m.dep_from) & (m.valid == True),
        c.second << (+m.dep_to) & (m.valid == True),
        c.third << (+m.dep_date) & (m.valid == True),
        c.fourth << (+m.dep_time) & (m.valid == True),
    )
    def confirm_all(c):
        print('Departing from {0} to {1} on {2} at {3}.'.format(
            c.first.dep_from,
            c.second.dep_to,
            c.third.dep_date,
            c.fourth.dep_time,
        ))


if __name__ == '__main__':
    # post('conversation', {
    #     'subject': ques[0],
    #     'value': input(ask_question() + '\n')
    # })
    post(
        'conversation', {
            'dep_from': 'Lon',
            'dep_to': 'Nor',
            'dep_date': 'New Years Eve',
            'dep_time': 'noon'
        })
    # pass