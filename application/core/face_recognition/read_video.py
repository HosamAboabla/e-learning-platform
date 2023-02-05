from application.core.face_recognition.emotion import detector
import cv2 as cv
from application.core.face_recognition.face import get_face_verification
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Display the resulting frame
    try:
        emotion = dict(detector.detect_emotions(frame)[0])['emotions']
        if emotion['neutral'] < 0.8:
            emotion['neutral'] = 0.0
        test = sorted(emotion.items(), key=lambda kv: (kv[1], kv[0]))
        emotion_name = test[-1][0]
    except:
        emotion_name = 'vide'
    if cv.waitKey(1) == ord('q'):
        face = get_face_verification(frame)
        face_frame = frame
        cv.putText(frame, str(face), (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (66, 66, 1), 2)
        cv.imshow('image_capture', frame)
    frame1 = cv.putText(frame, emotion_name, (0, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (66, 66, 1), 2)
    cv.imshow('frame', frame1)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
