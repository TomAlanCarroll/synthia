"""
    Synthia Controller
"""
from flask import Flask
import requests, json, audio_controller, config

app = Flask(__name__)

# Calls a function to get a customer morning message, then plays it
def play_morning_message():
    message = get_morning_message()
    audio_controller.play_message(message)


# Gets a custom morning message with helpful tips to start your day
def get_morning_message():
    message = 'Good morning! '

    result = requests.get(config.get("weather_endpoint"));
    content = result.content
    data = json.loads(content)

    weather_data = data.get('weather')
    current_weather = weather_data[0].get('main')
    current_weather_desc = weather_data[0].get('description')

    if current_weather:
        message += 'The current weather is ' + current_weather_desc + " in Berlin. "
        current_weather_reminder_message = get_current_weather_reminder_message(current_weather)

        if current_weather_reminder_message:
            message += current_weather_reminder_message

    message += 'Have a nice day and don\'t forget your keys!'

    return message


# Returns a message based off the current weather
def get_current_weather_reminder_message(current_weather):
    if current_weather == config.get("drizzle") or current_weather == config.get("rain"):
        return 'You should bring an umbrella. '

    if current_weather == config.get("sunny"):
        return 'You should wear sunglasses. '

    return ''


# Play a welcome home message
def play_evening_message():
    message = get_welcome_home_message()
    audio_controller.play_message(message)
    play_song()


# Get a custom welcome home message
def get_welcome_home_message(name = ''):
    message = 'Welcome home'

    if name:
      message += ', ' + name

    return message


# Play a mp3 music file
def play_song():
    audio_file = "songs/evening.mp3"
    audio_controller.play_audio_file(audio_file)

