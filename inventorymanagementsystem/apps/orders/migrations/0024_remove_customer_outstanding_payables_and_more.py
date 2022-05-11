# Generated by Django 4.0.3 on 2022-05-10 05:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_alter_invoice_payment_deadline'),
        ('orders', '0023_alter_order_delivery_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='outstanding_payables',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='outstanding_payables',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default=datetime.date(2022, 5, 25)),
        ),
        migrations.AlterField(
            model_name='order',
            name='invoice',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.invoice'),
        ),
    ]
