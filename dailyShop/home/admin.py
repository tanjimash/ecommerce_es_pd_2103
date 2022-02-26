from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'prod_name', 'prod_desc', 'prod_price']
    list_display_links = ['prod_name']
    pass


admin.site.register(Product, ProductAdmin)
