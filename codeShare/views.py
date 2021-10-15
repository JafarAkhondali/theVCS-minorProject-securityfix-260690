from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, HttpResponse
import json
import os
from .models import Code
from accounts.models import Profile
from GoogleDriver.gdrive import GoogleDriver
from minorProject.settings import GDRIVE_BASE_FOLDER
import uuid

# Create your views here.

def formatDate(date):
    return "{} {}, {}".format(str(date.day), str(date.strftime('%B')[:3]), str(date.year)[2:])


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }

    return render(request, 'codeShare/home.html', context)


def editCode(request):
    if request.user.is_authenticated == False:
        return HttpResponse(json.dumps({"status": "failed"}))
    if request.method == "POST":
        gdrive = GoogleDriver(GDRIVE_BASE_FOLDER)
        title = request.POST.get("title")
        codeSettings = json.loads(request.POST.get("codeSettings"))
        data = request.POST.get("data")
        pkey = request.POST.get("pkey")
        mode = request.POST.get("mode")

        # updating database
        code = Code.objects.get(pk=pkey)

        if code.owner != request.user:
            return HttpResponse(json.dumps({"status": "unauthorised user"}))

        code.codeName = title
        code.codeSettings = codeSettings
        code.lastEditTime = datetime.now(tz=timezone.utc)
        code.save()

        # updating user
        profile = Profile.objects.filter(user=request.user).first()

        if profile is None:
            return HttpResponse(json.dumps({"error": "User not found"}))

        profile.codes.add(code)
        profile.lastSettings = codeSettings
        profile.lastMode = mode
        profile.lastCode = pkey
        profile.save()

        # updating drive
        gid = code.driveId
        gdrive.editFile(GDRIVE_BASE_FOLDER, pkey, data)

        return HttpResponse(json.dumps({"status": "success"}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def saveCode(request):
    if request.user.is_authenticated == False:
        return HttpResponse(json.dumps({"status": "failed"}))

    if request.method == "POST":
        gdrive = GoogleDriver(GDRIVE_BASE_FOLDER)
        title = request.POST.get("title")
        codeSettings = json.loads(request.POST.get("codeSettings"))
        data = request.POST.get("data")
        pkey = request.POST.get("pkey")
        mode = request.POST.get("mode")

        if pkey != "0":
            editCode(request)
        else:
            profile = Profile.objects.filter(user=request.user).first()

            if profile is None:
                return HttpResponse(json.dumps({"error": "User not found"}))

            pkey = uuid.uuid4().hex
            gid = gdrive.uploadData(GDRIVE_BASE_FOLDER, pkey, data)
            code = Code.create(pkey=pkey, codeName=title,
                               codeSettings=codeSettings, owner=request.user, driveId=gid)

            profile.codes.add(code)
            profile.lastSettings = codeSettings
            profile.lastMode = mode
            profile.lastCode = pkey
            profile.save()
        return HttpResponse(json.dumps({"status": "success", "pkey": pkey}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getCode(request):
    if request.method == "POST":
        gdrive = GoogleDriver(GDRIVE_BASE_FOLDER)
        pkey = request.POST.get("pkey")
        code = Code.objects.get(pk=pkey)

        if not code:
            return HttpResponse(json.dumps({"error": "no such code"}))

        context = {}

        context["data"] = gdrive.readFile(GDRIVE_BASE_FOLDER, code.codeId)
        context["owner"] = code.owner.username
        context["dateOfCreation"] = formatDate(code.dateOfCreation)
        context["lastEditTime"] = formatDate(code.lastEditTime)
        context["codeName"] = code.codeName
        context["mode"] = json.loads(json.dumps(code.codeSettings))["mode"]

        return HttpResponse(json.dumps(context))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))

# if __name__ == "__main__":
