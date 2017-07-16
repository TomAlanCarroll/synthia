import snowboydecoder
import sys
import signal
import config
from threading import Thread

def interrupt_callback():
    return False

def listen_for_wakeword():
	model = config.get('snowboy_model')

	detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

	print('Listening... Press Ctrl+C to exit')
	detector.start(detected_callback=snowboydecoder.play_audio_file_and_record,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

	detector.terminate()

# main loop
wakeword_thread = Thread(target = listen_for_wakeword)
wakeword_thread.daemon = True
wakeword_thread.start()
