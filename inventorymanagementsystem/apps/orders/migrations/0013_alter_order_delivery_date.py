# Generated by Django 4.0.3 on 2022-05-04 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.date(2022, 5, 19)),
        ),
    ]
