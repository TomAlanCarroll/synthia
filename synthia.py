from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, world, v7.'


@app.route('/get_morning_message', methods=['POST'])
def get_morning_message():
    message = 'Not post'

    if request.method == 'POST':
        message = 'Post'

    return message