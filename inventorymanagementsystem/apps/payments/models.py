from django.db import models

from ..orders.models import Order

class Invoice(models.Model):

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_date = models.DateField()
    payment_deadline = models.DateField()
    payment_status = models.BooleanField(default=True ,null=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

class Payment(models.Model):

    payee_name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
