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

def stringToRGB(base64_string):
    encoded_data = base64_string.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def getRGB(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def rgb_to_hex(color):
  return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def getColors(img):
    colLmt = 10
    img = getRGB(stringToRGB(img))

    # resizing the image to decrese processing time
    img = cv2.resize(img, (300, 200), interpolation=cv2.INTER_AREA)
    df = img.reshape(img.shape[0] * img.shape[1], 3)

    # plt.imshow(img)
    # plt.show()

    km = KMeans(n_clusters=colLmt)
    predicted = km.fit_predict(df)
    
    cnt = {}

    for i in range(colLmt):
        cnt[i] = 0

    for i in predicted:
        cnt[i] += 1
    
    center_colors = km.cluster_centers_
    ordered_colors = [center_colors[i] for i in cnt.keys()]
    hex_colors = [rgb_to_hex(ordered_colors[i]) for i in cnt.keys()]
    context = {
        "color": hex_colors,
        "colorCnt": [i for i in cnt.values()],
    }
    return context


if __name__ == "__main__":
    print("prince is my name")