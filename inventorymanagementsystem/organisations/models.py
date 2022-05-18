import uuid
from django.db import models

# Create your models here.
class Organisation(models.Model):

    organisation_uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name