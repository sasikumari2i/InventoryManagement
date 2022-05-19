import uuid
from django.core.validators import RegexValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.db import models
from datetime import date, timedelta

from ..products.models import Product
from ..payments.models import Invoice
from utils.constants import ValidationConstants
from organisations.models import Organisation


class Vendor(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    vendor_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(
        max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX]
    )
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class Customer(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    customer_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    address = models.CharField(max_length=400, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(
        max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX]
    )
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class Order(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    order_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateField(default=date.today)
    delivery_date = models.DateField(default=(date.today() + timedelta(days=15)))
    delivery_status = models.BooleanField(default=False)
    vendors = models.ForeignKey(
        Vendor,
        to_field="vendor_uid",
        db_column="vendor_uid",
        default=None,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    invoice = models.ForeignKey(
        Invoice,
        models.SET_NULL,
        to_field="invoice_uid",
        db_column="invoice_uid",
        related_name="orders",
        default=None,
        null=True,
        blank=True,
    )
    updated_date = models.DateField(default=date.today)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return "Purchase Order"


class OrderProduct(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    product = models.ForeignKey(
        Product,
        to_field="product_uid",
        db_column="product_uid",
        related_name="products",
        on_delete=models.DO_NOTHING,
    )
    order = models.ForeignKey(
        Order,
        to_field="order_uid",
        db_column="order_uid",
        related_name="order_products",
        on_delete=models.CASCADE,
        null=True,
    )
    quantity = models.IntegerField(null=True)
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    # organisation_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = [["product", "order"]]
