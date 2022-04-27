from django.core.validators import RegexValidator
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from utils.constants import ValidationConstants


class Category (SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product (SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=400, null=True)
    available_stock = models.IntegerField(default=0)
    price = models.FloatField()
    category = models.ForeignKey(Category,related_name='categories',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
