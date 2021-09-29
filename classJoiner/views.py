from django.shortcuts import render, HttpResponse
import json
import string 
import joblib
# Create your views here.
def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'classJoiner/home.html', context)


def getclasses(request):
    if request.method=='POST':
        with open("./classJoiner/artifact/timetable.json") as f:
            _index = json.load(f)
        group=request.POST.get('group')
        day=request.POST.get('day')
        period=request.POST.get('period')
        period=int(float(period))
        dic=dict()
        if period>=9 or period<0 or len(_index[group][day][period])==1:
            dic={
                "teacher":"NO CLASS",
                "subject":"NOW YOU ARE FREE",
                "link":"javascript:void(0)"
            }
        else:
            dic={
                "teacher":_index[group][day][period][0],
                "subject":_index[group][day][period][1],
                "link":_index[group][day][period][2]
            }
        return HttpResponse(json.dumps(dic))
    else:
        return HttpResponse(json.dumps({"status":"failed"}))

    

