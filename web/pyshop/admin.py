from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display=['name','category','price_is']
    prepopulated_fields = {"slug": ("name",)}


class CartAdmin(admin.ModelAdmin):
    list_display=['item','user','created']

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered']



admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Checkout)



# Register your models here.
