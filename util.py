# from matplotlib import pyplot as plt
import joblib
import json
import numpy as np
import base64
import cv2
from keras_facenet import FaceNet
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
detector = MTCNN()

embedder = FaceNet()


def get_embedding(face_img):
    face_img = face_img.astype('float32')  # 3D
    face_img = np.expand_dims(face_img, axis=0)  # 4D
    # 4D (None x 160 x 160)
    yhat = embedder.embeddings(face_img)
    return yhat[0]


def get_faces(image_path, img64data):
    print(image_path)
    if (image_path is not None):
        img = cv2.imread(image_path)
    else:
        img = get_image_from_base64(img64data)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cropped_faces = []

    for faces in detector.detect_faces(img):
        x, y, w, h = faces['box']
        t_im = img[y:y+h, x:x+w]
        t_im = cv2.resize(t_im, (160, 160))
        cropped_faces.append(t_im)

    return cropped_faces


def classify_image(image64data, filepath=None):
    # imgs = get_crop_image_2_eyes(filepath, image64data)
    imgs = get_faces(filepath, image64data)
    celebs = []
    for img in imgs:
        # plt.imshow(img)
        # plt.show()
        t_im = cv2.resize(img, (160, 160))
        test_im = get_embedding(t_im)
        test_im = [test_im]
        celeb = __model.predict(test_im)
        prob = __model.predict_proba(test_im)*100
        print(celeb)
        celebs.append({
            'celeb': celeb_name(celeb[0]),
            'cid': str(celeb[0]),
            'score': np.round(np.max(prob), 2),
            'proba': np.round(prob*100, 2).tolist()[0],
            'dict': __name_2_number

        })
    return celebs


def celeb_name(celeb_num):
    return __number_2_name[celeb_num]


def get_celeb_names():
    return __number_2_name


def load_artifacts():
    print('loading artifacts..')
    global __model
    global __name_2_number
    global __number_2_name

    with open('./artifacts/class_dict_all.json', 'r') as f:
        __name_2_number = json.load(f)

        __number_2_name = {v: k for k, v in __name_2_number.items()}

    with open('./artifacts/face_net_model.pkl', 'rb') as f:
        __model = joblib.load(f)

    print('artifacts..loaded')


def get_image_from_base64(base64_text):
    enc_data = base64_text.split(',')[1]
    npar = np.frombuffer(base64.b64decode(enc_data), np.uint8)
    img = cv2.imdecode(npar, cv2.IMREAD_COLOR)
    return img


def get_crop_image_2_eyes(image_path, img64data):
    face_cascade = cv2.CascadeClassifier(
        './opencv/haarcascades/haarcascade_frontalface_default.xml')

    eye_cascade = cv2.CascadeClassifier(
        './opencv/haarcascades/haarcascade_eye.xml')

    if (image_path is not None):
        img = cv2.imread(image_path)
    else:
        img = get_image_from_base64(img64data)

    # plt.imshow(img)
    # plt.show()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # if (len(faces) == 0):
    #     print('no face detected')
    # print(faces)
    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_org = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if (len(eyes) >= 2):
            # print(roi_org)
            # plt.imshow(roi_org)
            # plt.show()
            cropped_faces.append(roi_org)

    return cropped_faces


def get_b64_text():
    # filename='messi64.txt'
    # filename = 'viratmessi64_2.txt'
    filename = 'viratmesi64.txt'
    with open(filename) as f:
        return f.read()


if __name__ == '__main__':

    load_artifacts()
    # classify_image(get_b64_text(), filepath=None)
    # aishwarya.jpeg')
    # prd = classify_image(
    #     None, filepath='brad.webp')
    # for s in prd:
    #     print(s.get('celeb'), s.get('score'))
    #     # print(classify_image(None, filepath='aishwarya.jpeg'))
    # print(classify_image(None, filepath='messi-and-kohli.png'))

    # for c in celebs:
    #     print(c)
