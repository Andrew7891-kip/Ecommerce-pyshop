from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

CATEGORY=(
    ('shirt','shirt'),
    ('sportswear','sportswear'),
    ('outwear','outwear'),
)

class Product(models.Model):
    name=models.CharField(max_length=60)
    category=models.CharField(max_length=10,choices=CATEGORY)
    photo=models.ImageField(upload_to='images')
    price_is=models.FloatField()
    describtion=models.TextField()
    price_was=models.FloatField()
    slug=models.SlugField()


    def saving(self):
        return (self.price_was - self.price_is)


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.quantity} of {self.item.name} '

    def get_total(self):
        return self.quantity * self.item.price_is

    


class Order(models.Model):
    orderitems=models.ManyToManyField(Cart)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    ordered=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    checkout=models.ForeignKey('Checkout',on_delete=models.CASCADE,blank=True,null=True) 

    def __str__(self):
        self.user.username

    def get_grand_total(self):
        total=0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        return total 


class Checkout(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    county=models.CharField(max_length=60)
    country=CountryField()
    address=models.CharField(max_length=60)
     
    def __str__(self):
        return self.user.username


