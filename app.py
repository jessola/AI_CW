from flask import Flask
from flask_socketio import SocketIO, send, emit

from conversation2 import Engine
from journeys import get_journeys, get_all_journeys, at_station

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
io = SocketIO(app)

e = Engine()
e.reset()


def handle_statement(text):
    # print(text)
    emit('message', text)


@io.on('connect')
def init_engine():
    e.init_output_statement(handle_statement)
    e.init_output_question(handle_statement)
    e.run()


@io.on('received')
def listen(data):
    e.listen(data)


# def test():
#     e.init_output_statement(lambda x: io.send('message', x, json=True))
#     e.init_output_question(lambda x: io.send('message', x, json=True))

if __name__ == "__main__":
    # To start the conversation, type 'ticket' at the first prompt
    # e = Engine()
    # e.reset()
    # e.init_output_statement(lambda x: test(x))
    # e.init_output_question(lambda x: test(x))
    # e.init_output_statement(lambda x: print(x))
    # e.init_output_question(lambda x: e.listen(input(x)))
    # e.run()

    # at_station('DISS')
    io.run(app)
