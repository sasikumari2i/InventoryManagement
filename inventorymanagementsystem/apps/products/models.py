from django.core.validators import RegexValidator

from django.db import models


class ValidationConstants:
    """Regex Validator strings defined here"""

    NAME_REGEX = RegexValidator(r'[A-Za-z]+([ ][a-zA-Z]+)*', 'Enter a valid name')


class Category (models.Model):
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product (models.Model):
    name = models.CharField(max_length=100, validators=[ValidationConstants.NAME_REGEX])
    description = models.CharField(max_length=400)
    available_stock = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
