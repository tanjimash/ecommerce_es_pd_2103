from django.shortcuts import render
from .models import *
from cartOrder.models import *

# Create your views here.


def homepage(request):
	product = Product.objects.all()

	context = {
		'product' : product
	}

	return render(request, 'home/homepage.html', context)


def prodDetails(request, id):
	prod = Product.objects.get(pk=id)
	cart = Cart.objects.all()
	print(cart)
	context = {
	'prod' : prod,
	'cart':cart
	}

	return render(request, 'home/productDetail.html', context)
	pass