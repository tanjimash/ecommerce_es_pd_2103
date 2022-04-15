from django.contrib import admin
from .models import Product

# to see product meaningful
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id', 'prod_name', 'prod_desc', 'prod_img_url', 'prod_price', 'prod_img']
	list_display_links = ['prod_name']

# Register your models here.
admin.site.register(Product, ProductAdmin)