"""
    Synthia
    ~~~~~~
    The Synthetic Intelligent Assistant for your home
"""
from flask import Flask
import weather, requests, json, play_audio

app = Flask(__name__)


# Calls a function to get a customer morning message, then plays it
def play_morning_message():
    message = get_morning_message()
    play_audio.play_message(message)


# Gets a custom morning message with helpful tips to start your day
def get_morning_message():
    message = 'Good morning! '

    result = requests.get(weather.API_END_POINT);
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
    return {
        weather.DRIZZLE or weather.RAINING: 'Don\'t forget your umbrella. ',
        weather.SUNNY: 'You should wear sunglasses. ',
    }.get(current_weather, '')


# Play a welcome home message
def play_evening_message():
    message = get_welcome_home_message()
    play_audio.play_message(message)


# Get a custom welcome home message
def get_welcome_home_message():
    return 'Welcome home.'


# Play a mp3 or m4a file
def play_song():
    audio_file = "songs/evening.m4a"
    play_audio(audio_file)