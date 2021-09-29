from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('apis/', include('apis.urls')),
    path('olympiansRecognizer/', include('olympiansRecognizer.urls')),
    path('colorsInImage/', include('colorsInImage.urls')),
    path('homePricePrediction/', include('homePricePrediction.urls')),
    path('jsonConvertor/', include('jsonConvertor.urls')),
    path('stockSentimentAnalysis/', include('stockSentimentAnalysis.urls')),
]
