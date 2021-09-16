from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
import json
import base64
from sklearn.cluster import KMeans
import cv2
import numpy as np

# Create your views here.

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


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'colorsInImage/home.html', context)


def findColors(request):
    if request.method == "POST":
        img_data = request.POST.get("img_data")
        return HttpResponse(json.dumps(getColors(img_data)))
    else:
        return HttpResponse(json.dumps({"status": "failes"}))