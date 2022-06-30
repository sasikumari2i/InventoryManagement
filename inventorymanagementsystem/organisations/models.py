import uuid
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from datetime import date


class Organisation(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    organisation_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True)
    created_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    created_by = models.UUIDField(default=None, null=True)

    def __str__(self):
        return self.name
