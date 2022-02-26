from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'customer', 'is_purchased', 'total_cart_items', 'total_price']
    list_display_links = ['cart_id']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cartItem_id', 'cart', 'product', 'cartItem_quantity', 'cartItem_price']
    list_display_links = ['cartItem_id']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'cart_id', 'price', 'payment_method', 'is_paid', 'is_cancelled', 'delivery_address', 'delivery_time']
    list_display_links = ['order_id']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)

