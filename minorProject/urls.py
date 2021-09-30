from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('apis/', include('apis.urls')),
    path('olympiansRecognizer/', include('olympiansRecognizer.urls')),
    path('colorsInImage/', include('colorsInImage.urls')),
    path('homePricePrediction/', include('homePricePrediction.urls')),
    path('jsonConvertor/', include('jsonConvertor.urls')),
    path('stockSentimentAnalysis/', include('stockSentimentAnalysis.urls')),
    path('classJoiner/', include('classJoiner.urls')),

    url(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
