# Generated by Django 4.0.3 on 2022-05-10 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_remove_customer_outstanding_payables_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='vendor',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='vendor',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]