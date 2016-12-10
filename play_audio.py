import sys
import os.path
import os
from gtts import gTTS
from subprocess import call
from playsound import playsound


def play_audio_file(audio_file):
    """
    Plays audio file default audio device
    """

    print "Input audio file: " + audio_file

    file_name = os.path.splitext(audio_file)[0]
    extension = os.path.splitext(audio_file)[1]
    print "file name: " + file_name
    print "extension: " + extension

    # convert m4a file to mp3
    if extension == ".m4a":
        m4a_audio_file = audio_file
        audio_file = "/tmp/audio.mp3"

        print "converting file..."
        call(["ffmpeg", "-i", m4a_audio_file, audio_file])
        print "done converting file."

    # linux2 matches RPi system
    if sys.platform == "linux2":
        # using shell call as quick a dirty way to play mp3 on a raspberry pi
        print "playing audio file: " + audio_file
        call(["mpg321", audio_file])

    else:
        print "playing audio file: " + audio_file
        playsound(audio_file)


def play_message(message, language="en-us"):
    """
    Plays message as audio through default audio device
    """
    audio_mp3_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_mp3_file)

    play_audio_file(audio_mp3_file)

