from django.db import models

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
    
