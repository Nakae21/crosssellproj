from django.contrib import admin
from .models import Product, Department, Aisle, Order, OrderProduct

admin.site.register(Product)
admin.site.register(Department)
admin.site.register(Aisle)
admin.site.register(Order)
admin.site.register(OrderProduct)
