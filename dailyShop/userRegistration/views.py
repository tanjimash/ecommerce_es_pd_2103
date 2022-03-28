from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from cartOrder.models import Cart
from .forms import *



def registration(request):
    print('User registration function is called!')

    # for u in dir(User):
    #     print(u)

    # Render an empty form
    form = UserRegForm()

    if request.method == 'POST':
        form = UserRegForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('userRegApp:signin')

    context = {
        'form': form,
    }
    return render(request, 'userRegistration/user_reg.html', context)





def signin(request):
    print('Login Function is called!')

    # Render an empty form
    form = UserLoginForm()

    if request.method == 'POST':
        # print(request.POST)
        user_name = request.POST['username']
        password = request.POST['password']
        # print(password)
        user = authenticate(request, username=user_name, password=password)
        # print(user)
        if user is not None:
            # print(user.username, '-------', user.email)
            login(request, user)
            # return HttpResponse(f'Logged in as: {user.username}!')
            return redirect('homeApp:homepage')

    context = {
        'form': form,
    }

    return render(request, 'userRegistration/user_login.html', context)
    pass




def user_logout(request):
    logout(request)
    return redirect('userRegApp:signin')

