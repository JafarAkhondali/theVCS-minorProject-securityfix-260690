from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
import pandas as pd
import json
import joblib
import numpy as np

# Create your views here.
model = None
X = None



def load_saved_data():
    global model
    global X

    X = pd.read_csv("homePricePrediction/artifacts/my_file.csv")
    model = joblib.load("homePricePrediction/artifacts/model.pkl")




def getAddress(request):
    if request.method == "POST":
        with open('homePricePrediction/artifacts/address.json', 'r') as openfile:
            json_object = json.load(openfile)
        return HttpResponse(json.dumps(json_object))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))




def predictPrice(postedBy, underConstruction, rera, bhk, bhk_or_rk, sqrtFt, readyToMove, resale, longitude, latitude, address):
    load_saved_data()
    x = np.zeros(len(X.columns))

    # print(postedBy, underConstruction, rera, bhk, bhk_or_rk, sqrtFt, readyToMove, resale, longitude, latitude, address)

    # filling data
    x[0] = underConstruction
    x[1] = rera
    x[2] = bhk
    x[3] = bhk_or_rk
    x[4] = sqrtFt
    x[5] = readyToMove
    x[6] = resale
    x[7] = longitude
    x[8] = latitude

    try:
        x[X.columns.get_loc(postedBy)] = 1
    except:
        pass

    try:
        x[X.columns.get_loc(address)] = 1
    except:
        pass

    res = model.predict([x])[0]

    if res < 0:
        return json.dumps({"result": "No such house exists"})

    return json.dumps({"result": "Estimated Price Is {:.2f} Lakh Rupees".format(res)})




def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'homePricePrediction/home.html', context)




def getPrice(request):
    if request.method == "POST":
        underConstruction = request.POST.get("underConstruction")
        rera = request.POST.get("rera")
        bhk = request.POST.get("bhk")
        bhk_or_rk = request.POST.get("bhkOrRk")
        sqrtFt = request.POST.get("sqFt")
        readyToMove = request.POST.get("readyToMove")
        resale = request.POST.get("resaled")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        postedBy = request.POST.get("postedBy")
        address = request.POST.get("address")
        return HttpResponse(predictPrice(postedBy, underConstruction, rera, bhk, bhk_or_rk, sqrtFt, readyToMove, resale, longitude, latitude, address))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))
