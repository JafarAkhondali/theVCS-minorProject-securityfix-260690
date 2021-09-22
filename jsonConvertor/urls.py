from django.contrib import admin
from django.urls import path, include
from jsonConvertor import views

urlpatterns = [
    path('',views.home,name='jsonConvertor'),
    path('PunctuationRemover/',views.PunctuationRemover,name='PunctuationRemover'),
    path('ToUpperConvertor/',views.ToUpperConvertor,name='ToUpperConvertor'),
    path('LineRemover/',views.LineRemover,name='LineRemover'),
    path('ExtraSpaceRemover/',views.ExtraSpaceRemover,name='ExtraSpaceRemover'),
    path('JSONconvertor/',views.JSONconvertor,name='JSONconvertor'),
]