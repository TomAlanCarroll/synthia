import speech_recognition as sr
import config
import json

def recognize_speech():
	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)

	try:
		print("Starting speech recognition")
		cred_json = json.loads(open(config.get('google_cloud_api_service_account_json')).read())
		recognized_speech = r.recognize_google_cloud(audio, credentials_json=cred_json)
		# we need some special handling here to correctly print unicode characters to standard output
		if str is bytes:  # this version of Python uses bytes for strings (Python 2)
			print(u"You said {}".format(recognized_speech).encode("utf-8"))
		else:  # this version of Python uses unicode for strings (Python 3+)
			print("You said {}".format(recognized_speech))
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
