from flask import Flask, request, jsonify
import pusher

from conversation2 import Engine
from journeys import get_journeys, get_all_journeys, at_station

app = Flask(__name__)
# e = Engine()
# e.reset()

# Pusher Config
pusher_client = pusher.Pusher(
    app_id='928615',
    key='99815334007378cc329d',
    secret='07df68ecb505a9f822db',
    cluster='eu',
    ssl=True,
)

e = Engine()
e.reset()


def output_statement(text):
    pusher_client.trigger('my-channel', 'statement', {'message': text})


def output_question(text):
    pusher_client.trigger('my-channel', 'question', {'message': text})


e.init_output_statement(output_statement)
e.init_output_question(output_question)
e.run()

# e = Engine()
# e.reset()
# e.init_output_statement(output_statement)
# e.init_output_question(output_question)
# e.run()


@app.route('/', methods=['POST'])
def user_message():
    try:
        message = request.json['data']
        e.listen(message['text'])
        # e.reset()
        e.run()

        return jsonify({'success': True}), 200
    except:
        print('FAILED')

    return jsonify({'success': False}), 400


# def test():
#     e.init_output_statement(lambda x: io.send('message', x, json=True))
#     e.init_output_question(lambda x: io.send('message', x, json=True))

if __name__ == "__main__":
    # To start the conversation, type 'ticket' at the first prompt
    # e = Engine()
    # e.reset()
    # e.init_output_statement(output_statement)
    # e.init_output_question(output_question)
    # e.run()
    # e.init_output_statement(lambda x: test(x))
    # e.init_output_question(lambda x: test(x))
    # e.init_output_statement(lambda x: print(x))
    # e.init_output_question(lambda x: e.listen(input(x)))
    # e.run()

    # at_station('DISS')

    app.run(debug=True)