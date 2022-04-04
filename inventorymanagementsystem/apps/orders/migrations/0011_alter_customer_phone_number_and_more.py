# Generated by Django 4.0.3 on 2022-04-01 03:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_vendor_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[6-9][0-9]{9}', 'Enter a valid phone number')]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[6-9][0-9]{9}', 'Enter a valid phone number')]),
        ),
    ]