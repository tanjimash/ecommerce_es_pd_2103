from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, server = CartItem)
def update_cart(server, **kwargs):
    print('Cart update signal is called!')
    print('Cart item called!', kwargs['instance'])

    cartItemInstance = kwargs['instance']
    print('Cart item id: ', cartItemInstance.cartItem_id)

    cartID = cartItemInstance.cart.cart_id
    cartItem_quantity = cartItemInstance.cartItem_quantity
    cartItem_price = cartItemInstance.cartItem_price

    cart = Cart.objects.get(cart_id=cartID)

    cart.total_price += cartItem_price
    cart.total_cart_items += cartItem_quantity

    pass
