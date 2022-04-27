import datetime
from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.db import models

from utils.constants import ValidationConstants


class Invoice(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_date = models.DateField(default=datetime.date.today, null=True)
    payment_deadline = models.DateField()
    payment_status = models.BooleanField(default=False ,null=True)


class Payment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    payment_types = (
        (1, "Cheque"),
        (2, "Cash"),
        (3, "Digital"),
    )

    payee_name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    created_date = models.DateField(default=datetime.date.today)
    payment_type = models.IntegerField(choices=payment_types,default=2)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX])
    amount = models.BigIntegerField(default=0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

