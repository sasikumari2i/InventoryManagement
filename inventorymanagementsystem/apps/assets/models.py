import uuid
from django.db import models
from datetime import date, timedelta
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from ..products.models import Product, Inventory
from ..orders.models import Customer
from utils.constants import ValidationConstants
from organisations.models import Organisation


# Create your models here.
class Asset(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    asset_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    inventory = models.ForeignKey(
        Inventory,
        to_field="inventory_uid",
        db_column="inventory_uid",
        on_delete=models.DO_NOTHING,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        to_field="customer_uid",
        db_column="customer_uid",
    )
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True, null=False)
    return_date = models.DateField(default=None, null=True)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class RepairingStock(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    repairing_stock_uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.DO_NOTHING, to_field="asset_uid", db_column="asset_uid"
    )
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    closed_date = models.DateField(default=None, null=True)
    organisation = models.ForeignKey(
        Organisation,
        to_field="organisation_uid",
        db_column="organisation_uid",
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return "Repairing Stock"