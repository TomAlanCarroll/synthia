from flask import Flask, request, weather, requests, json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, my name is Synthia, the Synthetic Intelligent Assistant for your home'


@app.route('/get_morning_message', methods=['POST'])
def get_morning_message():
    message = 'Good morning!'

    result = requests.get(weather.API_END_POINT);
    content = result.content

    data = json.loads(content)
    weather_data = data.get('weather')
    current_weather = weather_data[0].get('main')

    if current_weather:
        message += 'The current weather is ' + current_weather
        current_weather_reminder_message = get_current_weather_reminder_message(current_weather)

        if current_weather_reminder_message:
            message += current_weather_reminder_message

    message += ' Have a nice day!'

    return message

def get_current_weather_reminder_message(current_weather):
    return {
        weather.RAINING: ' Blah.',
        weather.DRIZZLE: ' Don\'t forget your umbrella.',
        weather.SUNNY: ' You should wear sunglasses.',
    }.get(current_weather, '')


print get_morning_message();