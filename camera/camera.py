from PIL import Image
import io
import picamera
import time


CAMERA_RESOLUTION_X = 100
CAMERA_RESOLUTION_Y = 100
CAPTURE_WAIT_TIME = 5
CAPTURE_PX_DELTA_THRESHOLD = 20
CAPTURE_PXS_DELTA_THRESHOLD = 25


def camera_capture():
    """
    Capture an image into a byte stream.
    """
    camera = picamera.PiCamera()

    # capture an image into a byte stream
    stream = io.BytesIO()
    camera.capture(stream, format='bmp')

    stream.seek(0)
    img = Image.open(stream)
    img_buffer = img.load()
    stream.close()

    return img, img_buffer


def camera_detect_motion():
    """
    Determine whether motion was detected between two images.
    """
    # capture control image
    img1, img_buffer1 = camera_capture()

    # while True:
    time.sleep(CAPTURE_WAIT_TIME)

    # capture different image
    img2, img_buffer2 = camera_capture()

    # determine difference
    pxs_delta = 0
    for x in xrange(0, CAMERA_RESOLUTION_X):
        for y in xrange(0, CAMERA_RESOLUTION_Y):
            px_delta = abs(img_buffer1[x, y][1] - img_buffer2[x, y][1])
            if px_delta > CAPTURE_PX_DELTA_THRESHOLD:
                pxs_delta += 1

    # if we see enough of a difference, break out of the loop
    # if pxs_delta > CAPTURE_PXS_DELTA_THRESHOLD:
    #     break

    # this function should return when motion is detected
    return True


def main():
    print "Hello."
    camera_detect_motion()


if __name__ == '__main__':
    main()
