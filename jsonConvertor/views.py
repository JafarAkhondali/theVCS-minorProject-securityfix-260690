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
        intext= request.POST.get('text','no text enter')
        
        result=intext

        analysed=""
        for char in result:
            if char not in string.punctuation:
                analysed=analysed+char
        result=analysed

      
        
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))

def toupperconvertor(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')
        
        result=intext

        analysed=""
        analysed=analysed+intext.upper()
        result="on"
        result=analysed

      
        
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))