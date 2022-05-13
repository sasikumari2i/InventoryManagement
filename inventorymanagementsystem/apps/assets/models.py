from django.db import models
from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.db import models
from datetime import date, timedelta

from ..products.models import Product
from ..orders.models import Customer
from ..payments.models import Invoice
from utils.constants import ValidationConstants
from organisations.models import Organisation

# Create your models here.
class Asset(models.Model):


    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    serial_no = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, null=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class RepairingStock(models.Model):

    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    serial_no = models.CharField(max_length=100)
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name
