from fer import FER
from application.core.image.image_refactor import stringToRGB

detector = FER()


class Emotion:
    dict_emotion = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0.1}
    dict_level = {'neutral': 'n1', 'fear': 'n1', 'sad': 'n1', 'happy': 'n3', 'surprise': 'n4', 'angry': 'n2',
                  'disgust': 'n2'}

    def get_emotion(self, image_base64):
        header, image_base64 = image_base64.split(",", 1)
        image_base64 = stringToRGB(image_base64)
        try:
            emotion = dict(detector.detect_emotions(image_base64)[0])['emotions']
            if emotion['neutral'] < 0.8:
                emotion['neutral'] = 0.0
            test = sorted(emotion.items(), key=lambda kv: (kv[1], kv[0]))
            emotion_name = test[-1][0]
        except:
            emotion_name = 'vide'
        return emotion_name

    def get_emotion_predict(self, image_base64):
        try:
            for image in image_base64:
                emotion = self.get_emotion(image)
                self.dict_emotion[emotion] = self.dict_emotion[emotion] + 1
        except:
            pass

    def get_level_evaluation(self):
        emotion = sorted(self.dict_emotion.items(), key=lambda kv: (kv[1], kv[0]))[-1][0]
        self.dict_emotion = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0.1}
        return emotion, self.dict_level[emotion]
