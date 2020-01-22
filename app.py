from flask import Flask, request, jsonify
import pusher

from conversation2 import Engine
from conversation4 import ChatBot
from journeys import get_journeys, get_all_journeys, at_station

app = Flask(__name__)

# Pusher Config
pusher_client = pusher.Pusher(
    app_id='928615',
    key='99815334007378cc329d',
    secret='07df68ecb505a9f822db',
    cluster='eu',
    ssl=True,
)


def output_statement(text):
    pusher_client.trigger('my-channel', 'statement', {'message': text})


def output_question(text):
    pusher_client.trigger('my-channel', 'question', {'message': text})


# Set up the bot
bot = ChatBot(output_statement, output_question)
bot.reset()


@app.route('/', methods=['POST'])
def user_message():
    try:
        message = request.json['data']
        bot.listen(message['text'])
        bot.run()

        return jsonify({'success': True}), 200
    except:
        print('FAILED')

    return jsonify({'success': False}), 400


if __name__ == "__main__":
    bot.run()

    app.run(debug=True)