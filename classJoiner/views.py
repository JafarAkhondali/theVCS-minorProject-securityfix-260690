from django.shortcuts import render, HttpResponse
import json
import pandas as pd
from twilio.rest import Client

# Create your views here.


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'classJoiner/home.html', context)


def getclasses(request):
    if request.method == 'POST':
        with open("./classJoiner/artifacts/timetable.json") as f:
            _index = json.load(f)

        group = request.POST.get('group')
        day = request.POST.get('day')
        period = request.POST.get('period')
        period = int(float(period))
        dic = dict()
        if period >= 9 or period < 0 or len(_index[group][day][period]) == 1:
            dic = {
                "teacher": "NO CLASS",
                "subject": "NOW YOU ARE FREE",
                "link": "javascript:void(0);"
            }
        else:
            dic = {
                "teacher": _index[group][day][period][0],
                "subject": _index[group][day][period][1],
                "link": _index[group][day][period][2]
            }
        return HttpResponse(json.dumps(dic))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def sendMessage(request):
    if request.method == 'POST':
        df = pd.read_csv("./classJoiner/artifacts/phoneNo.csv",
                         encoding='utf-8-sig')

        with open("./classJoiner/artifacts/secrets.json") as f:
            secret = json.load(f)

        account_sid = secret["accountSid"]
        auth_token = secret["auth_token"]
        client = Client(account_sid, auth_token)

        with open("./classJoiner/artifacts/timetable.json") as f:
            _index = json.load(f)

        day = request.POST.get('day')
        period = request.POST.get('period')
        period = int(float(period))

        # getting link of all the classes
        l1 = l2 = l3 = l4 = None

        if period >= 9 or period < 0:
            l1 = "No class now"
            l2 = "No class now"
            l3 = "No class now"
            l4 = "No class now"
        else:
            # G1
            if len(_index["G1"][day][period]) == 1:
                l1 = "No class now"
            else:
                l1 = _index["G1"][day][period][2]

            # G2
            if len(_index["G2"][day][period]) == 1:
                l2 = "No class now"
            else:
                l2 = _index["G2"][day][period][2]

            # G1
            if len(_index["G3"][day][period]) == 1:
                l3 = "No class now"
            else:
                l3 = _index["G3"][day][period][2]

            # G1
            if len(_index["G4"][day][period]) == 1:
                l4 = "No class now"
            else:
                l4 = _index["G4"][day][period][2]

        text = "G1: {}\nG2: {}\nG3: {}\nG4: {}".format(l1, l2, l3, l4)

        for phoneNo in df["phoneNo"]:
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=text,
                to='whatsapp:+{}'.format(str(phoneNo))
            )

        return HttpResponse(json.dumps({"status": "passed"}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


if __name__ == "__main__":
    sendMessage()
