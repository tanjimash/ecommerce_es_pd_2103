from django.shortcuts import render, redirect, HttpResponse
from .models import *
from home.models import *
from django.urls.base import reverse

# Payment Gateway Integration
# SSLCommerz
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt



"""
SSLCommerz Implementation Ref:    https://www.youtube.com/watch?v=krTt8Xdchow
"""



def addToCart(request):
    print('Add to cart function is called!')

    # Construct you logic here
    # ------------
    if request.method == "POST":
        print('Product ID:', request.POST['prod_id'])
        print('Cart ID:', request.POST['cart_id'])
        print('Product Quantity:', request.POST['prod_quantity'])

        cart = Cart.objects.get(cart_id=request.POST['cart_id'])
        product = Product.objects.get(pk=request.POST['prod_id'])
        print('Cart Record (after query):', cart)
        print('Cart Record (after query):', cart.cart_id)
        print('Product Record (after query):', product)


        # make a condition to check if any other same product exist in the cart
        cart_item_duplicate = CartItem.objects.filter(product=product)

        # print('Duplicate CartItem ("Add To Cart" function):', cart_item_duplicate)

        if len(cart_item_duplicate) == 0:
            print('#'*50)
            print('New cart item is created!')
            CartItem.objects.create(
                cart=cart,
                product=product,
                cartItem_quantity=int(request.POST['prod_quantity'])
            )
            print('#'*50)
        else:
            print('#'*50)
            print('Duplicate cart item is found!')
            for cit_dup in cart_item_duplicate:
                cit_dup.cartItem_quantity += int(request.POST['prod_quantity'])
                cit_dup.save()
            print('#'*50)


    # ##########################

    # return redirect('homeApp:homepage')
    # return HttpResponse('Add to cart function is called!')
    return redirect(reverse(
        'cartOrderApp:cart',
        kwargs={'cart_id': cart.cart_id}
    ))



def cart(request, cart_id):
    cart = Cart.objects.get(cart_id=cart_id)
    cartItems = CartItem.objects.filter(cart=cart)

    for cit in cartItems:
        print(cit)

    context = {
        'title': 'Cart',
        'cart': cart,
        'cart_id': cart_id,
        'cartItems': cartItems,
    }
    return render(request, 'cartOrder/cart.html', context)
    pass



def cartItem_remove(request, cit_id):
    print('CartItem remove is called!')

    print('Cart Item ID:', cit_id)
    #
    cartItem_record = CartItem.objects.get(cartItem_id=cit_id)
    # print('Cart Item ID (after query):', cartItem_record.cartItem_id)
    print('Cart ID (after "CartItem" query):', cartItem_record.cart.cart_id)

    cartItem_record.delete()

    cart_record = Cart.objects.get(cart_id=cartItem_record.cart.cart_id)
    # print('Cart ID (after "Cart" query):', cart_record.cart_id)

    # return HttpResponse({
    #     'msg': 'Cart remove function is called!',
    #     'CartItem_ID': cit_id,
    # })
    # return redirect("")
    return redirect(reverse(
        'cartOrderApp:cart',
        kwargs={'cart_id': cart_record.cart_id}
    ))
    pass






def createOrder(request, cart_id):
    if request.method == 'POST':
        # print('Cart ID:', cart_id)

        cart = Cart.objects.get(cart_id=cart_id)
        # print('Cart (order function):', cart)
        cartItems = CartItem.objects.filter(cart=cart)

        for cit in cartItems:
            print('cart item (order function):', cit)

        cust = User.objects.get(username=request.user)
        # print('customer (order function):', cust)


        # Check if any order of "not-cancelled" & "not-paid" exists
        order = Order.objects.filter(customer=cust, cart_id=cart, is_paid=False, is_cancelled=False)

        # print('createOrder function --- Order:', order)
        if len(order) == 0:
            # create the order
            # print('Create Order function -- A new order is created! Then it will be redirected to the order_summary page!')
            Order.objects.create(
                customer=cust,
                cart_id=cart,
                price=cart.total_price,
            )
        else:
            # update the order regarding the cart
            # print('Create Order function -- The order record is updated! Then it will be redirected to the order_summary page!')
            # order_total_price = 0
            for o in order:
                # print('Create Order function -- Order ID:', o.order_id)
                # print('Create Order function -- Cart Price:', o.cart_id.total_price)
                o.price = o.cart_id.total_price
                o.save()

    return redirect(reverse(
        'cartOrderApp:order_summary',
        kwargs={'cart_id': cart_id}
    ))




def order_summary(request, cart_id):
    print('#'*50)
    print('Order Summary function is called! Cart ID:', cart_id)

    cart = Cart.objects.get(cart_id=cart_id)
    # print('Cart (order Summary function):', cart)
    cartItems = CartItem.objects.filter(cart=cart)
    # print('Cart Items (order Summary function):', cartItems)
    cust = User.objects.get(username=request.user)
    order = Order.objects.get(customer=cust, cart_id=cart, is_paid=False, is_cancelled=False)
    print('Order:', order)
    print('#' * 50)

    context = {
        'title': 'Order Page',
        'cart_id': cart_id,
        'cartItems': cartItems,
        'order': order,
    }
    return render(request, 'cartOrder/order.html', context)
    pass





def order_cancel(request, order_id):
    print('order_cancel function -- order id:', order_id)
    order = Order.objects.get(order_id=order_id)
    print('order_cancel function -- order (after query):', order)
    order.is_cancelled = True
    order.save()
    return redirect('homeApp:homepage')
    # return HttpResponse('The order is cancelled!')




def placeOrder_cod(request, order_id):
    if request.method == "POST":
        print('Order is placed! (COD). Order ID:', order_id)
        order = Order.objects.get(order_id=order_id)
        order.payment_method = 'COD'
        order.save()
        return HttpResponse('Order is placed! (COD)')





def placeOrder_sslcommerz(request, order_id):
    if request.method == "POST":
        print('Order is placed! (SSLCommerz). Order ID:', order_id)
        order = Order.objects.get(order_id=order_id, is_paid=False, is_cancelled=False)
        # order.payment_method = 'SSLCommerz'
        # order.save()

        print('Order Total Price ("placeOrder_sslcommerz" func):', order.price)
        print('Order Total Item Quantity ("placeOrder_sslcommerz" func):', order.cart_id.total_cart_items)

        order_price = order.price
        order_quantity = order.cart_id.total_cart_items

        store_id = 'creat621675119a224'
        store_pass = 'creat621675119a224@ssl'

        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                                sslc_store_pass=store_pass)

        status_url = request.build_absolute_uri(reverse('cartOrderApp:sslc_status'))
        mypayment.set_urls(success_url=status_url, fail_url=status_url,
                           cancel_url=status_url, ipn_url=status_url)

        mypayment.set_product_integration(total_amount=Decimal(order_price), currency='BDT', product_category='None',
                                          product_name='demo-product', num_of_item=order_quantity,
                                          shipping_method='YES', product_profile='None')
        customer = request.user
        print('Customer name:', customer.username)

        # for d in dir(customer):
        #     print( d )

        mypayment.set_customer_info(name=customer.username, email=customer.email, address1='demo address',
                                    address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh',
                                    phone='01711111111')
        mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209',
                                    country='Bangladesh')
        response_data = mypayment.init_payment()

        print('#'*50)
        print('Response Data:', response_data)
        print('#'*50)
        return redirect(response_data['GatewayPageURL'])
    #     return redirect('cartOrderApp:sslc_status')
    # return HttpResponse('Order is placed! (SSLCommerz)')





@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        print('='*50)
        print('sslc_status method:',payment_data)

        print('sslc_status method (status):', payment_data['status'])
        status = payment_data['status']
        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']

            return redirect(reverse(
                'cartOrderApp:sslc_complete',
                kwargs={'val_id': val_id, 'tran_id': tran_id}
            ))

        print('='*50)
        return render(request, 'sslcommerz/status.html')
    pass


def sslc_complete(request, val_id, tran_id):
    order = Order.objects.filter(customer=request.user, is_paid=False, is_cancelled=False).first()
    print('sslc_complete method ("Order" query):', order)

    # modify the 'Order' record
    order.is_paid = True
    order.order_id = val_id
    order.transaction_id = tran_id
    order.save()

    # modify the 'Cart' record
    cart = Cart.objects.get(cart_id=order.cart_id.cart_id, is_purchased=False)
    cart.is_purchased = True
    cart.save()
    print('sslc_complete method ("Cart" query):', cart)

    return redirect('homeApp:homepage')
    # return HttpResponse(f'Order Payment is complete! Order ID: {val_id} ------ Trans ID: {tran_id}')


