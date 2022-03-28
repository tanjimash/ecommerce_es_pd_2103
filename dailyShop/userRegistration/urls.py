from django.urls import path
from . import views


app_name = 'userRegApp'



urlpatterns = [
    path('user-registration/', views.registration, name='registration'),
    path('user-sign-in/', views.signin, name='signin'),
    path('user-sign-out/', views.user_logout, name='logout'),
]
