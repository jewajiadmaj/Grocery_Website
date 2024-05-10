from django.contrib import admin
from .models import Category,Product,Unit,Customer,Order,Notification,Charge
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Charge)

