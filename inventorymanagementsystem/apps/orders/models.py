import datetime
from django.core.validators import RegexValidator

from django.db import models
from ..products.models import Product


class ValidationConstants:
    """Regex Validator strings defined here"""

    PHONE_NUMBER_REGEX = RegexValidator(r'[6-9][0-9]{9}', 'Enter a valid phone number')
    NAME_REGEX = RegexValidator(r'[A-Za-z]+([ ][a-zA-Z]+)*', 'Enter a valid name')


class Vendor (models.Model):

    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])

    def __str__(self):
        return self.name


class Customer (models.Model):
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=400)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])

    def __str__(self):
        return self.name


class Order (models.Model):
    is_sales_order = models.BooleanField(default=True ,null=False)
    order_date = models.DateField(default=datetime.date.today)
    delivery_date = models.DateField()
    #products = models.ManyToManyField(Product, through='OrderProduct',related_name='products')
    vendors = models.ForeignKey(Vendor,related_name='orders',on_delete=models.CASCADE, null=True, blank=True)
    customers = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.is_sales_order:
            return "Sales Order"
        else:
            return "Purchase Order"


class OrderProduct(models.Model):

    product = models.ForeignKey(Product,related_name='products',on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='orderproducts',on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        unique_together = [['product','order']]
