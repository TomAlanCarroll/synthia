import sys
import vlc
from gtts import gTTS
from subprocess import call
from playsound import playsound

# Plays audio file default audio device
def play_audio_file(audio_file):
    p = vlc.MediaPlayer(audio_file)
    p.play()

# Plays message as audio through default audio device
def play_message(message, language="en-us"):
    audio_mp3_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_mp3_file)

    play_audio_file(audio_mp3_file)

