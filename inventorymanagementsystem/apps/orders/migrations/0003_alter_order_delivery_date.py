# Generated by Django 4.0.3 on 2022-05-19 04:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_customer_organisation_alter_order_invoice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.date(2022, 6, 3)),
        ),
    ]