from django.contrib import admin
from .models import Category, Product, ProductDetail, BagItem, OrderItem, Order, Coupon
# Register your models here.


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(BagItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)





