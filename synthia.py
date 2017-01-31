"""
    Synthia Image Detection Server
"""
from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import MotionSensor
from face import detection
import imutils
import time
import cv2
import datetime
import synthia_controller
import config

# PIR output should be connected to GPIO 4
pir_sensor_detection = config.get("pir_sensor_detection")
pir = None
if pir_sensor_detection:
    print "[INFO] Initializing PIR sensor..."
    pir = MotionSensor(4)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(config.get("resolution"))
camera.framerate = config.get("fps")
rawCapture = PiRGBArray(camera, size=tuple(config.get("resolution")))
morning_time_min = config.get("morning_time_min")
morning_time_max = config.get("morning_time_max")
morning_reminder_message = config.get("morning_reminder_message")
evening_time_min = config.get("evening_time_min")
evening_time_max = config.get("evening_time_max")
evening_song_path = config.get("evening_song_path")
city = config.get("city")
postal_code = config.get("postal_code")
morning_start = datetime.time(morning_time_min)
morning_end = datetime.time(morning_time_max)
evening_start = datetime.time(evening_time_min)
evening_end = datetime.time(evening_time_max)
morning_message_played = 0
evening_message_played = 0

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] Starting camera server..."
time.sleep(config.get("camera_warmup_time"))
avg = None
lastUploaded = datetime.datetime.now()
pir_detection_period_seconds = 6
motionCounter = 0
motion_detection_counter = 1
now = datetime.datetime.now()
endScanTime = now

if pir is not None:
    print "[INFO] Waiting for PIR warmup..."

# Main control loop for processing camera images
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and status text
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "No movement"
    # resize the frame
    frame = imutils.resize(frame, width=500)
    now = datetime.datetime.now()
    if (not pir_sensor_detection or (pir is not None and pir.motion_detected)) or now < endScanTime:
        motion_detection_counter += 1
        print "[INFO] Motion detected within the past " + str(pir_detection_period_seconds) + " seconds; counter: " + str(motion_detection_counter)
        endScanTime = now + datetime.timedelta(seconds=pir_detection_period_seconds)

        # convert it to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detection.detect_multi(gray)

        if faces is not None and len(faces) > 0:
            for (x, y, w, h) in faces:
                # draw the face boundary(s) on the frame in blue
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            state = "Opening"

        # check to see if the room is opening
        if state == "Opening" and morning_start <= timestamp.time() <= morning_end \
                and morning_message_played < 1:
            synthia_controller.play_morning_message()
            morning_message_played = 1

        if state == "Opening" and evening_start <= timestamp.time() <= evening_end \
                and evening_message_played < 1:
            synthia_controller.play_evening_message()
            evening_message_played = 1

        if not morning_start <= timestamp.time() <= morning_end:
            morning_message_played = 0

        if not evening_start <= timestamp.time() <= evening_end:
            evening_message_played = 0

        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Door Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)

        # check to see if the room is opening for stream
        if state == "Opening":
            # check to see if enough time has passed between uploads
            if (timestamp - lastUploaded).seconds >= config.get("min_upload_seconds"):
                # increment the motion counter
                motionCounter += 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if motionCounter >= config.get("min_motion_frames"):
                    # update the last uploaded timestamp and reset the motion
                    # counter
                    lastUploaded = timestamp
                    motionCounter = 0

        # otherwise, the door is not opening
        else:
            motionCounter = 0

    # check to see if the frames should be displayed to screen
    if config.get("show_video"):
        # display the security feed
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
