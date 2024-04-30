from django.db import models
from datetime import date
# Create your models here.
class Customer(models.Model):
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.email
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100,blank=True)
    def __str__(self):
         return self.name

class Product(models.Model):
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    active = models.BooleanField(default=True)
    qty = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.title
    
class Order(models.Model):
    Orderplacedid=models.CharField(max_length=200,blank=True)
    Customer_id=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    mobile_number=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    product_id=models.CharField(max_length=200)
    product_name=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    product_sub_price=models.CharField(max_length=200)
    my_date = models.DateField(default=date.today)
    active = models.BooleanField(default=True)

class Notification(models.Model):
    email = models.EmailField(unique=True,blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.email
