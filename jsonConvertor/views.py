from django.shortcuts import render, HttpResponse
import json

# Create your views here.


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'jsonConvertor/home.html', context)


def punctuationRemover(request):
    if request.method == "POST":
        text = request.POST.get("text")
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        for x in text.lower():
            if x in punctuations:
                text = text.replace(x, "")

        return HttpResponse(json.dumps({"text": text}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))
