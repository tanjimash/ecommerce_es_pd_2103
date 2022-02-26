from django.db import models


class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    prod_desc = models.TextField()
    prod_price = models.FloatField(default=0.0)
    prod_image = models.ImageField(upload_to='prodImage', default='prodImage/default_prod_image.png', blank=True)

    class Meta():
        verbose_name_plural = 'Product'

