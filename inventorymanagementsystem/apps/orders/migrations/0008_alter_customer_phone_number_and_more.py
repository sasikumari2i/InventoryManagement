# Generated by Django 4.0.3 on 2022-03-31 17:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_customer_phone_number_alter_order_customers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('[6-9][0-9]{9}', 'only valid phonenumber is required')]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('[6-9][0-9]{9}', 'only valid phonenumber is required')]),
        ),
    ]