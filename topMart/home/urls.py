from django.contrib import admin
from django.urls import path

from . import views

app_name='homeApp'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('productdetail/<str:id>', views.prodDetails, name='prodDetails'),
]
