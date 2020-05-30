from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','register_date')

admin.site.register(Product, ProductAdmin)
