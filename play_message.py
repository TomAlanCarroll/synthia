import sys
from gtts import gTTS
from subprocess import call
from playsound import playsound


def play_message(message, language="en-us"):
    """
    Plays message as audio through default audio device
    """
    audio_mp3_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_mp3_file)
    #
    if sys.platform == "linux2":
        # using shell call as quick a dirty way to play mp3 on a raspberry pi
        call(["mpg321", audio_mp3_file])

    else:
        playsound(audio_mp3_file)
