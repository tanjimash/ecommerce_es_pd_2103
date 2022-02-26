from django.db import models
from django.contrib.auth.models import User
from home.models import Product
import random, string


def random_string_generator(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    total_cart_items = models.PositiveBigIntegerField(default=0)
    is_purchased = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        verbose_name_plural = 'Cart'

    def save(self, *args, **kwargs):
        # If no 'cart_id' isn't passed while creating an order.
        if not len(self.cart_id):
            self.cart_id = str(self.customer) + "_" + random_string_generator()
        super(Cart, self).save(*args, **kwargs)




class CartItem(models.Model):
    cartItem_id = models.CharField(max_length=100, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cartItem_quantity = models.PositiveBigIntegerField(default=0)
    cartItem_price = models.FloatField(default=0)

    class Meta():
        verbose_name_plural = 'Cart Item'

    def save(self, *args, **kwargs):
        # If no 'cart_id' isn't passed while creating an order.
        if not len(self.cartItem_id):
            self.cartItem_id = random_string_generator()

        self.cartItem_price = self.cartItem_quantity * self.product.prod_price

        super(CartItem, self).save(*args, **kwargs)





PAYMENT_CHOICES = [
    ('COD', 'COD'),
    ('SSLCommerz', 'SSLCommerz'),
]
class Order(models.Model):
    order_id = models.CharField(verbose_name='Order ID', max_length=100)
    transaction_id = models.CharField(verbose_name='Transaction ID', max_length=255, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer+', verbose_name='Customer')
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=PAYMENT_CHOICES, default='COD')
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    delivery_address = models.TextField(verbose_name="Delivery Address", blank=True)
    delivery_time = models.DateField(verbose_name='Delivery Time', auto_now_add=True)

    class Meta:
        verbose_name_plural = "Order"

    def __str__(self) -> str:
        return self.order_id

    def save(self, *args, **kwargs):
        # If no 'order_id' isn't passed while creating an order, then auto-generate the id using randomizer.
        if not len(self.order_id):
            self.order_id = 'order_' + str(self.customer) + "_" + random_string_generator()

        super(Order, self).save(*args, **kwargs)



