# Generated by Django 4.0.3 on 2022-05-23 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_order_invoice'),
        ('payments', '0006_alter_invoice_organisation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(blank=True, db_column='order_uid', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoices', to='orders.order', to_field='order_uid'),
        ),
    ]
