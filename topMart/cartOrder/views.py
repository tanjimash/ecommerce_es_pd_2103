from django.shortcuts import render, redirect
from .models import *
from home.models import *


# Create your views here.
def addToCart(request):
    print('d to cart hitted.')

    if request.method == "POST":
    	print("prod Id: ", request.POST['prod_id'])
    	# print("prod Id: ", request.POST['prod_des'])
    	# print("card Id: ", request.POST['cart_id'])
    	# print("prod quantity: ", request.POST['prod_quantity'])


    	# cart = Cart.objects.get(cart_id = request.POST['cart_id'])
    	product = product.objects.get(pk=request.POST['prod_id'])

    	# print('CCart', cart)
    	print('Prod', product)

    return redirect('homeApp:homepage')
    
    # 	cart = Cart.objects.get(cart_id=request.POST[cart_id])