# from flask import Flask, weather, requests, json
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, my name is Synthia, the Synthetic Intelligent Assistant for your home'
#
#
# @app.route('/get_morning_message', methods=['POST'])

# Gets a custom morning message with helpful tips to start your day
import weather, requests, json, play_message
def get_morning_message():
    message = 'Good morning! '

    result = requests.get(weather.API_END_POINT);
    content = result.content
    data = json.loads(content)

    weather_data = data.get('weather')
    current_weather = weather_data[0].get('main')
    current_weather_desc = weather_data[0].get('description')

    if current_weather:
        message += 'The current weather is ' + current_weather_desc + ". "
        current_weather_reminder_message = get_current_weather_reminder_message(current_weather)

        if current_weather_reminder_message:
            message += current_weather_reminder_message

    message += 'Have a nice day!'

    return message

# Returns a message based off the current weather
def get_current_weather_reminder_message(current_weather):
    return {
        weather.DRIZZLE or weather.RAINING: 'Don\'t forget your umbrella. ',
        weather.SUNNY: 'You should wear sunglasses. ',
    }.get(current_weather, '')


# Calls a function to get a customer morning message, then plays it
def play_morning_message():
    message = get_morning_message()
    play_message.play_message(message)

print play_morning_message();