from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='stockSentimentAnalysis'),
    path('predictStocks/',views.predictStocks, name='predictStocks'),
    path('getHeadlines/',views.getHeadlines, name='getHeadlines'),
]