from django.db import models
import datetime

from ..orders.models import Order

class Invoice(models.Model):

    amount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    created_date = models.DateField(default=datetime.date.today)
    payment_deadline = models.DateField()
    payment_status = models.BooleanField(default=False ,null=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

class Payment(models.Model):

    payee_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
