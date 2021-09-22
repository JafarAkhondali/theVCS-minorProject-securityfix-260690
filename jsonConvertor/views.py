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
        repunc=request.GET.get('removepunc','off')
        upercase=request.GET.get('capital','off')
        endline=request.GET.get('endline','off')
        extraspace=request.GET.get('extraspace','off')

        analysed=""
        result=intext

        if repunc=='on':
            analysed=""
            for char in result:
                if char not in string.punctuation:
                    analysed=analysed+char
            result=analysed

        if upercase=="on":
            analysed=""
            analysed=analysed+result.upper()
            result=analysed

        if endline=="on":
            analysed=""
            for char in result:
                if char!="\n" and char!="\r":
                    analysed=analysed+char
            result=analysed

        if extraspace=="on":
            analysed=""
            for index,char in enumerate(result):
                if not(result[index]==" "and result[index+1]==" "):
                    analysed=analysed+char
            result=analysed
        
        return HttpResponse(json.dumps({"result": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))