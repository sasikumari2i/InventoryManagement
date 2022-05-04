from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.db import models
from datetime import date, timedelta

from ..products.models import Product
from ..payments.models import Invoice
from utils.constants import ValidationConstants


class Vendor (SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])

    def __str__(self):
        return self.name


class Customer (SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=400, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])
    wallet = models.BigIntegerField(default=100000)


    def __str__(self):
        return self.name


class Order (SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    is_sales_order = models.BooleanField(default=True ,null=False)
    order_date = models.DateField(default=date.today)
    delivery_date = models.DateField(default=(date.today() + timedelta(days=15)))
    delivery_status = models.BooleanField(default=False)
    vendors = models.ForeignKey(Vendor,default=None,on_delete=models.CASCADE, null=True, blank=True)
    customers = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE, blank=True, null=True)
    invoice = models.OneToOneField(Invoice, models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        if self.is_sales_order:
            return "Sales Order"
        else:
            return "Purchase Order"


class OrderProduct(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    product = models.ForeignKey(Product,related_name='products',on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, related_name='order_products',on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        unique_together = [['product','order']]
