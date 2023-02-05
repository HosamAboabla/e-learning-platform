import cv2
import fitz
import base64
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier('application/data_base/data/haarcascade_frontalface_default.xml')


def get_image_doc(base64_string):
    image_save = False
    img_np = stringToRGB(base64_string)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        image_save = True
    return image_save


def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(fitz.io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
