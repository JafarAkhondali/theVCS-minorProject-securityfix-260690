from django.shortcuts import render, HttpResponse
import json
import string 
# Create your views here.
def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'jsonConvertor/home.html', context)


def PunctuationRemover(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')
        result=""
        for char in intext:
            if char not in string.punctuation:
                result=result+char
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))
        

def ToUpperConvertor(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')
        result=""
        result=result+intext.upper()
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))



def LineRemover(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')        
        result=""
        for char in intext:
            if char!="\n" and char!="\r":
                result=result+char
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def ExtraSpaceRemover(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')        
        result=""
        for index,char in enumerate(intext):
            if not(intext[index]==" "and intext[index+1]==" "):
                result=result+char
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))



def JSONconvertor(request):
    if request.method == "POST":
        intext= request.POST.get('text','no text enter')        
        result=json.dumps(intext)
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))

