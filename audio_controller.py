import sys
import os.path
import os
from gtts import gTTS
from subprocess import call
from playsound import playsound

# Plays audio file default audio device
def play_audio_file(audio_file):
    # linux2 matches RPi system
    if sys.platform == "linux2":
        # using shell call as quick a dirty way to play mp3 on a raspberry pi
        print "playing audio file: " + audio_file
        call(["mpg321", audio_file])

    else:
        print "playing audio file: " + audio_file
        playsound(audio_file)

# Plays message as audio through default audio device
def play_message(message, language="en-us"):
    audio_mp3_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_mp3_file)

    play_audio_file(audio_mp3_file)

