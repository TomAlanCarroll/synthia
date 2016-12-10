from gtts import gTTS
from subprocess import call


def play_message(message, language="en-us"):
    """
    Plays message as audio through default audio device
    """
    audio_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_file)

    # using shell call as quick a dirty way to play mp3 on a raspberry pi
    call(["omxplayer",audio_file])

