import uuid
from django.core.validators import RegexValidator
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from datetime import date, timedelta
from rest_framework.authtoken.models import Token

from organisations.models import Organisation
from utils.constants import ValidationConstants


class Category(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    category_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=200, null=True)
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    product_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=400, null=True)
    available_stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    category = models.ForeignKey(
        Category,
        to_field="category_uid",
        db_column="category_uid",
        related_name="categories",
        on_delete=models.CASCADE,
        null=True,
    )
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
