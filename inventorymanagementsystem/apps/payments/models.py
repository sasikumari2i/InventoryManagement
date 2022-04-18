import datetime
from django.core.validators import RegexValidator

from django.db import models
from utils.constants import ValidationConstants
from ..orders.models import Order


class Invoice(models.Model):

    amount = models.DecimalField(default=0,max_digits=10, decimal_places=2, null=True)
    created_date = models.DateField(default=datetime.date.today, null=True)
    payment_deadline = models.DateField()
    payment_status = models.BooleanField(default=False ,null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)


class Payment(models.Model):

    payee_name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
