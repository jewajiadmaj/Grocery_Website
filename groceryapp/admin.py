from django.contrib import admin
from .models import Category,Product,Unit,Customer,Order
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(Order)

