from django.shortcuts import render, redirect
from .models import *
from cartOrder.models import *
from django.contrib.auth.models import User


def homepage(request):
    prod = Product.objects.all()

    # print('User:', request.user)
    # print('User ID:', request.user.id)

    user = User.objects.get(pk=request.user.id)
    # print('User (after query):', user)
    # print('User Email (after query):', user.email)

    cart = Cart.objects.filter(customer=user, is_purchased=False).first()
    # print('Customer Cart:', cart)

    if cart == None:
        Cart.objects.create(customer=user)
        return redirect('homeApp:homepage')


    context = {
        'title': 'Homepage',
        'prod': prod,
        'cart': cart,
        'cart_id': cart.cart_id,
    }
    return render(request, 'home/homepage.html', context)


def prodDetail(request, id, cart_id):
    prod = Product.objects.get(pk=id)
    cart = Cart.objects.get(cart_id=cart_id, is_purchased=False)

    print('Cart ID (Product Detail Page):', cart)
    print('Product ID (Product Detail Page):', prod)


    context = {
        'prod': prod,
        'cart': cart,
        'cart_id': cart.cart_id,
    }
    return render(request, 'home/productDetail.html', context)



