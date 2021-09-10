from re import I
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
import matplotlib.pyplot as plt
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sn
#from sklearn import datasets
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import cv2
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import randint
from scipy.stats import norm
from openml import tasks, flows, runs, datasets, config
import random
from sklearn.pipeline import Pipeline
import json
import pywt
import base64
face_cascade = cv2.CascadeClassifier(
    './server/openCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(
    './server/openCV/haarcascades/haarcascade_eye.xml')

_model = None
_index = None
_names = []


def load_saved_artifacts():
    global _model
    global _index

    _model = joblib.load(
        "./server/artifacts/olympians_recognizer/model.pkl")
    with open("./server/artifacts/olympians_recognizer/name.json") as f:
        _index = json.load(f)

    for i, j in _index.items():
        _names.append(i)


def w2d(img, mode='haar', level=1):
    imArray = img
    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    imArray = np.float32(imArray)
    imArray /= 255
    coeffs = pywt.wavedec2(imArray, mode, level=level)

    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0

    imArray_H = pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)

    return imArray_H


def stringToRGB(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def cropImage(img):
    lst = []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if(len(eyes) >= 2):
            lst.append(roi_color)

    return lst


def classify_image(img_data):
    img = stringToRGB(img_data)
    img = cropImage(img)
    

    if(len(img) > 1):
        return {"err": "got more than one face"}

    if(len(img) == 0):
        return {"err": "got image without any face or without both eyes completely visible"}

    result = {}

    img = img[0]
    img = cv2.resize(img, (32, 32))
    img_wt = w2d(img)
    img_wt = cv2.resize(img_wt, (32, 32))
    combined_img = np.vstack(
        (img.reshape(32*32*3, 1), img_wt.reshape(32*32, 1)))
    combined_img = combined_img.reshape(1, 32*32*4).astype(float)
    result = {
        'class': _names[_model.predict(combined_img)[0]],
        'class_probability': np.around(_model.predict_proba(combined_img)*100, 2).tolist()[0],
        # 'class_dictionary': celeb_index
    }
    return result


if __name__ == "__main__":
    load_saved_artifacts()
    print(classify_image("prince"))
