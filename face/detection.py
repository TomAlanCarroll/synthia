import cv2
import config

haar_faces = cv2.CascadeClassifier(config.get("haar_cascades_file"))


def detect_single(image):
    """Return bounds (x, y, width, height) of detected face in grayscale image.
    If no face or more than one face are detected, None is returned.
    """
    faces = haar_faces.detectMultiScale(image,
                                        scaleFactor=config.get("haar_scale_factor"),
                                        minNeighbors=config.get("haar_min_neighbors"),
                                        minSize=config.get("haar_min_size"),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
    if len(faces) != 1:
        return None
    return faces[0]


def crop(image, x, y, w, h):
    """Crop box defined by x, y (upper left corner) and w, h (width and height)
    to an image with the same aspect ratio as the face training data.  Might
    return a smaller crop if the box is near the edge of the image.
    """
    crop_height = int((config.get("face_height") / float(config.get("face_width"))) * w)
    midy = y + h / 2
    y1 = max(0, midy - crop_height / 2)
    y2 = min(image.shape[0] - 1, midy + crop_height / 2)
    return image[y1:y2, x:x + w]


def resize(image):
    """Resize a face image to the proper size for training and detection.
    """
    return cv2.resize(image, (config.get("face_width"), config.get("face_height")), interpolation=cv2.INTER_LANCZOS4)