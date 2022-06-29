import uuid
from django.db import models
from datetime import date
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

from ..products.models import Inventory
from apps.orders.models import Employee
from organisations.models import Organisation


# Create your models here.
class Asset(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    asset_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    inventory = models.ForeignKey(
        Inventory,
        to_field="inventory_uid",
        db_column="inventory_uid",
        related_name='inventory',
        on_delete=models.DO_NOTHING,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
        to_field="employee_uid",
        db_column="employee_uid",
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
    asset = models.OneToOneField(
        Asset, on_delete=models.DO_NOTHING,
        unique=True,
        related_name='asset',
        to_field="asset_uid",
        db_column="asset_uid"
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