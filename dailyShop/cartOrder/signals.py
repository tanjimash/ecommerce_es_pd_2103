from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import *


@receiver(pre_delete, sender=CartItem)
def remove_cartItem(sender, **kwargs):
    print("A cart item is deleted!")
    cartItemInstance = kwargs['instance']
    cartID = cartItemInstance.cart.cart_id
    cartItem_quantity = cartItemInstance.cartItem_quantity
    cartItem_price = cartItemInstance.cartItem_price

    print("Cart Item quantity to be deleted: ", cartItem_quantity)
    print("Cart Item price to be decreased: ", cartItem_price)

    cart = Cart.objects.get(cart_id=cartID)

    print("Cart (Query):", cart)

    cart.total_price -= cartItem_price
    cart.total_cart_items -= cartItem_quantity

    cart.save()




@receiver(post_save, sender=CartItem)
def update_cart(sender, created, **kwargs):
    print('Cart Update signal is called!')
    print('Cart Item Instance', kwargs['instance'])
    cartItemInstance = kwargs['instance']
    print('Cart Item ID:', cartItemInstance.cartItem_id)

    cartID = cartItemInstance.cart.cart_id
    cartItem_quantity = cartItemInstance.cartItem_quantity
    cartItem_price = cartItemInstance.cartItem_price

    print('Cart Item Quantity:', cartItem_quantity)
    print('Cart Item Price:', cartItem_price)

    cart = Cart.objects.get(cart_id=cartID)

    cartItem = CartItem.objects.filter(cart_id=cart).last()

    totalQuantity = cartItem.cartItem_quantity

    print('Product Total Quantity:', totalQuantity)

    if created:
        print('Signal: New cartItem is created')
        cart.total_price += cartItem_price
        cart.total_cart_items += cartItem_quantity
    elif not created:
        print('Signal: Update is called!')

        cartItem_query = CartItem.objects.filter(cart_id=cart)

        update_cart_price = 0
        update_cart_quantity = 0
        print('Cart Item Query (Signal):', cartItem_query)
        for c_item in cartItem_query:
            print(f'CartItem Quantity: {c_item.cartItem_quantity} ------ CartItem Price: {c_item.cartItem_price}')
            update_cart_price += c_item.cartItem_price
            update_cart_quantity += c_item.cartItem_quantity

        print('Update Cart Price:', update_cart_price)
        print('Update Cart Quantity:', update_cart_quantity)

        cart.total_cart_items = update_cart_quantity
        cart.total_price = update_cart_price

    cart.save()

    print('Actual Cart:', cart)
    pass

