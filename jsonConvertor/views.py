from django.shortcuts import render, HttpResponse
import json
import string 

# Create your views here.


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'jsonConvertor/home.html', context)


def punctuationRemover(request):
    if request.method == "POST":
        text = request.POST.get("text")
        punctuations = string.punctuation
        result = ""

        for i in text:
            if i in punctuations or (len(result) and result[-1] == " " and i == " "):
                continue
            result += i
        print(result)
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))