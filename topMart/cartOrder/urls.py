from django.urls import path
from . import views

app_name = 'cartOrderApp'

urlpatterns = [
    path('addtocart/', views.addToCart, name='addCart'),
]