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

_olympians_recognizer_model = None
_olympians_recognizer_index = None


def load_saved_artifacts():
    global _olympians_recognizer_model
    global _olympians_recognizer_index


    _olympians_recognizer_model = joblib.load("./server/artifacts/olympians_recognizer/model.pkl")
    with open("./server/artifacts/olympians_recognizer/name.json") as f:
        _olympians_recognizer_index = json.load(f)


if __name__ == "__main__":
    load_saved_artifacts()
    print(_olympians_recognizer_index)
    print(_olympians_recognizer_model)
