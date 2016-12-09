from gtts import gTTS
from playsound import playsound


def play_message(message, language):
    audio_file = "/tmp/audio.mp3"
    text_to_message = gTTS(message, language)
    text_to_message.save(audio_file)
    playsound(audio_file)
