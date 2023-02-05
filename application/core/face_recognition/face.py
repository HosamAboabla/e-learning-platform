import face_recognition
from application.core.image.image_refactor import stringToRGB


def get_face_verification(unknown_image, known_image):
    try:
        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        dist = face_recognition.face_distance([biden_encoding], unknown_encoding)[0]
        if dist < 0.5:
            results = True
        else:
            results = False
    except:
        results = False
    return results


def face_base64(image1_base64, image2_base64):
    header, image1_base64 = image1_base64.split(",", 1)
    header, image2_base64 = image2_base64.split(",", 1)
    img_np1 = stringToRGB(image1_base64)
    img_np2 = stringToRGB(image2_base64)
    face_comparison = get_face_verification(img_np1, img_np2)
    return face_comparison
