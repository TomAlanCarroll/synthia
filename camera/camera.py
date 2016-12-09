import picamera


def camera_capture():
    camera = picamera.PiCamera()
    camera.capture('/tmp/image.jpg')


def main():
    print "Hello."
    camera_capture()


if __name__ == '__main__':
    main()
