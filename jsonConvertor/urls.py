from django.contrib import admin
from django.urls import path, include
from jsonConvertor import views

urlpatterns = [
    path('',views.home,name='jsonConvertor'),
    path('punctuationRemover/',views.punctuationRemover,name='punctuationRemover'),
    path('toupperconvertor/',views.toupperconvertor,name='toupperconvertor'),
]