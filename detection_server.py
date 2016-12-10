# import the necessary packages
# from pyimagesearch.tempimage import TempImage
# from dropbox.client import DropboxOAuth2FlowNoRedirect
# from dropbox.client import DropboxClient
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import datetime
import synthia

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
                help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
morning_time_min = conf["morning_time_min"]
morning_time_max = conf["morning_time_max"]
morning_reminder_message = conf["morning_reminder_message"]
evening_time_min = conf["evening_time_min"]
evening_time_max = conf["evening_time_max"]
evening_song_path = conf["evening_song_path"]
city = conf["city"]
postal_code = conf["postal_code"]
morning_start = datetime.time(morning_time_min)
morning_end = datetime.time(morning_time_max)
evening_start = datetime.time(evening_time_min)
evening_end = datetime.time(evening_time_max)
morning_message_played = 0
evening_message_played = 0

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print "[INFO] Starting camera server..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image and initialize
    # the timestamp and status text
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "No movement"

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the average frame is None, initialize it
    if avg is None:
        print "[INFO] Starting camera framing..."
        avg = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue

    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                           cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Opening"


    # check to see if the room is opening
    if text == "Opening" and morning_start <= datetime.datetime.now() <= morning_end \
            and morning_message_played < 1:
        synthia.play_morning_message()
        morning_message_played = 1

    if text == "Opening" and evening_start <= datetime.datetime.now() <= evening_end \
            and evening_message_played < 1:
        synthia.play_evening_message()
        evening_message_played = 1

    if not morning_start <= datetime.datetime.now() <= morning_end:
        morning_message_played = 0

    if not evening_start <= datetime.datetime.now() <= evening_end:
        evening_message_played = 0

    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Door Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # check to see if the room is opening for stream
    if text == "Opening":
        # check to see if enough time has passed between uploads
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            # increment the motion counter
            motionCounter += 1

            # check to see if the number of frames with consistent motion is
            # high enough
            if motionCounter >= conf["min_motion_frames"]:
                # check to see if dropbox sohuld be used
                if conf["use_dropbox"]:
                    '''
                    # write the image to temporary file
                    t = TempImage()
                    cv2.imwrite(t.path, frame)

                    # upload the image to Dropbox and cleanup the tempory image
                    print "[UPLOAD] {}".format(ts)
                    path = "{base_path}/{timestamp}.jpg".format(
                        base_path=conf["dropbox_base_path"], timestamp=ts)
                    client.put_file(path, open(t.path, "rb"))
                    t.cleanup()
                    '''

                # update the last uploaded timestamp and reset the motion
                # counter
                lastUploaded = timestamp
                motionCounter = 0

    # otherwise, the door is not opening
    else:
        motionCounter = 0

    # check to see if the frames should be displayed to screen
    if conf["show_video"]:
        # display the security feed
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)