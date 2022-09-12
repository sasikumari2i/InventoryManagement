import uuid
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

class Organisation(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    organisation_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Csv(models.Model):
    # _safedelete_policy = SOFT_DELETE_CASCADE

    # organisation_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    model_names = [
        ('Employee', 'Employee'),
    ]
    model = models.CharField(choices=model_names, default='READ', max_length=20)
    # name = models.CharField(max_length=100, unique=True)
    file = models.FileField()
    

    # def __str__(self):
    #     return self.name