from django.db import models

# Create your models here.

class Product(models.Model):
	prod_name = models.CharField(max_length = 150)
	prod_desc = models.TextField()
	prod_img_url = models.TextField()
	prod_price = models.FloatField(default=0.00)

	prod_img = models.ImageField(upload_to = 'prodImage', default = 'prodImage/default_img.png', blank=True)

	# for specify name in backend
	class Meta():
		verbose_name_plural = 'Products'

