from django.urls import path
from . import views

app_name = 'cartOrderApp'

urlpatterns = [
    path('add-to-cart/', views.addToCart, name='addToCart'),    # this need to be in the top
    path('<str:cart_id>/', views.cart, name='cart'),
    path('remove-cart-item/<str:cit_id>/', views.cartItem_remove, name='cartItem_remove'),

    path('create-order/<str:cart_id>/', views.createOrder, name='createOrder'),
    path('order-cancel/<str:order_id>/', views.order_cancel, name='order_cancel'),
    path('order-summary/<str:cart_id>/', views.order_summary, name='order_summary'),

    path('order-placement/cod/<str:order_id>/', views.placeOrder_cod, name='placeOrder_cod'),
    path('order-placement/sslcommerz/<str:order_id>/', views.placeOrder_sslcommerz, name='placeOrder_sslcommerz'),



    # SSLCommerz
    path('sslc/status/', views.sslc_status, name='sslc_status'),
    path('sslc/complete/<str:val_id>/<str:tran_id>/', views.sslc_complete, name='sslc_complete'),
]