from django.contrib import admin
from .models import *

# to see product meaningful
class CartAdmin(admin.ModelAdmin):
	list_display = ['cart_id', 'total_cart_items', 'total_price', 'customer']
	list_display_links = ['cart_id']


class CartItemAdmin(admin.ModelAdmin):
	list_display = ['cartItem_id', 'cart', 'product', 'cartItem_quantity', 'cartItem_price']
	list_display_links = ['cartItem_id']

# class DataManipulate(admin.ModelAdmin):
# 	list_display = ['cartItem_id', 'cart', 'product', 'cartItem_quantity', 'cartItem_price']
# 	list_display_links = ['cartItem_id']

# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
# admin.site.register(Data, DataManipulate)