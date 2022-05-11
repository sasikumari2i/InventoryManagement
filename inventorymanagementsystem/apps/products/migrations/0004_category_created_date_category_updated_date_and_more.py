# Generated by Django 4.0.3 on 2022-05-10 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='product',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
