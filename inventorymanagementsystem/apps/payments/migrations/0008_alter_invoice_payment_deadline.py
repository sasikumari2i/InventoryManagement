# Generated by Django 4.0.3 on 2022-05-04 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_invoice_payment_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_deadline',
            field=models.DateField(default=datetime.date(2022, 5, 19)),
        ),
    ]
