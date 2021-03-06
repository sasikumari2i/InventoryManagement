import uuid
import datetime
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.db import models
from datetime import date, timedelta
from organisations.models import Organisation
from utils.constants import ValidationConstants
from ..orders.models import Order


class Invoice(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    invoice_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_date = models.DateField(default=datetime.date.today, null=True)
    payment_deadline = models.DateField(default=(date.today() + timedelta(days=15)))
    payment_status = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(
        Order,
        models.SET_NULL,
        to_field="order_uid",
        db_column="order_uid",
        related_name="invoices",
        default=None,
        null=True,
        blank=True,
    )
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )


class Payment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    payment_types = (
        (1, "Cheque"),
        (2, "Cash"),
        (3, "Digital"),
    )

    payment_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payee_name = models.CharField(
        max_length=100, validators=[ValidationConstants.NAME_REGEX]
    )
    created_date = models.DateField(default=datetime.date.today)
    payment_type = models.IntegerField(choices=payment_types, default=2)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10, validators=[ValidationConstants.PHONE_NUMBER_REGEX]
    )
    amount = models.BigIntegerField(default=0)
    invoice = models.ForeignKey(
        Invoice,
        to_field="invoice_uid",
        db_column="invoice_uid",
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )
