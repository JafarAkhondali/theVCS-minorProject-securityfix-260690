from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'jsonConvertor/home.html', context)