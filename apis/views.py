from django import http
from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
import json


# add all ml projects here
ml_box = {
    "Olympians Recognizer": "/olympiansRecognizer",
    "Colors In Image": "/colorsInImage",
}

# add all tool box projects here
tool_box = {
}


# Create your views here.
def AllMlProjects(request):
    return HttpResponse(json.dumps(ml_box))

def AllToolBox(request):
    return HttpResponse(json.dumps(tool_box))
