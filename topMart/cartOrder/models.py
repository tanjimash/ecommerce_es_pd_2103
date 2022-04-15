from django.db import models
from django.contrib.auth.models import User
from home.models import Product
import random, string


def random_id_generator(size=20, chars= string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))



# Create your models here.

class Cart(models.Model):
	cart_id = models.CharField(max_length = 200, blank = True)
	total_cart_items = models.PositiveBigIntegerField(default = 0)
	total_price = models.FloatField(default = 0)
	customer = models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta():
		verbose_name_plural = 'Cart'		

	def save(self, *args, **kwargs):
		self.cart_id = str(self.customer) + '_' + random_id_generator()
		super(Cart,self).save(*args, **kwargs)


class CartItem(models.Model):
	cartItem_id = models.CharField(max_length = 200, blank = True)
	cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	cartItem_quantity = models.PositiveBigIntegerField(default = 0)
	cartItem_price = models.FloatField(default = 0)

	class Meta():
		verbose_name_plural = 'Cart Items'

	def save(self, *args, **kwargs):
		if not len(self.cartItem_id):
			self.cartItem_id =  random_id_generator()

		print('price', self.product.prod_price)

		# update price
		self.cartItem_price = self.cartItem_quantity * self.product.prod_price
		super(CartItem,self).save(*args, **kwargs)



# class Data(models.Model):
# 	cartItem_id = models.CharField(max_length = 200, blank = True)
# 	cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
# 	product = models.ForeignKey(Product, on_delete = models.CASCADE)
# 	cartItem_quantity = models.PositiveBigIntegerField(default = 0)
# 	cartItem_price = models.FloatField(default = 0)


# 	class Meta():
# 		verbose_name_plural = 'Data'