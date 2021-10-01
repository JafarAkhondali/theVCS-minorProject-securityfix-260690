from django.shortcuts import render, HttpResponse
import json
import string
import joblib
import tensorflow as tf
import numpy as np
# Create your views here.


def load_artifacts():
    scaler = joblib.load("./salaryPredictor/artifacts/scaler.pkl")
    model = tf.keras.models.load_model("./salaryPredictor/artifacts/model")

    return scaler, model


def readJSON(fileName):
    with open("./salaryPredictor/artifacts/"+fileName) as f:
        _index = json.load(f)
    return _index



def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'salaryPredictor/home.html', context)


def getWorkClass(request):
    if request.method == "POST":
        _index = readJSON("workClass.json")
        return HttpResponse(json.dumps({"workClass": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getEducation(request):
    if request.method == "POST":
        _index = readJSON("education.json")
        return HttpResponse(json.dumps({"education": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getMartialStatus(request):
    if request.method == "POST":
        _index = readJSON("martialStatus.json")
        return HttpResponse(json.dumps({"martialStatus": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getOccupation(request):
    if request.method == "POST":
        _index = readJSON("occupation.json")
        return HttpResponse(json.dumps({"occupation": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getRelationship(request):
    if request.method == "POST":
        _index = readJSON("relationship.json")
        return HttpResponse(json.dumps({"relationship": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getRace(request):
    if request.method == "POST":
        _index = readJSON("race.json")
        return HttpResponse(json.dumps({"race": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getCountry(request):
    if request.method == "POST":
        _index = readJSON("native_country.json")
        return HttpResponse(json.dumps({"country": _index}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def predict(request):
    if request.method == "POST":
        age, workclass, fnlwgt, education, maritalStatus, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country = request.POST("age"), request.POST("workclass"), request.POST("fnlwgt"), request.POST("education"), request.POST(
            "maritalStatus"), request.POST("occupation"), request.POST("relationship"), request.POST("race"), request.POST("sex"), request.POST("capital_gain"), request.POST("capital_loss"), request.POST("hours_per_week"), request.POST("native_country")

        scaler, model = load_artifacts()
        col_index = readJSON("colIndex.json")
        education_num = readJSON("education_num.json")

        x = np.zeros(100)
        sex = int(sex == "male")

        x[0] = age

        try:
            x[col_index[workclass]] = 1
        except:
            pass

        x[1] = fnlwgt

        try:
            x[2] = education_num[education]
        except:
            pass

        try:
            x[col_index[maritalStatus]] = 1
        except:
            pass

        try:
            x[col_index[occupation]] = 1
        except:
            pass

        try:
            x[col_index[relationship]] = 1
        except:
            pass

        try:
            x[col_index[race]] = 1
        except:
            pass

        x[3] = sex
        x[4] = capital_gain
        x[5] = capital_loss
        x[6] = hours_per_week

        try:
            x[col_index[native_country]] = 1
        except:
            pass

        x = scaler.transform([x])
        result = int(model.predict(x)[0][0] > 0.5)
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))
