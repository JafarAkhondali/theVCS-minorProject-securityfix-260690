from django.shortcuts import render, HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


# Create your views here.


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'home/home.html', context)

