# Generated by Django 4.0.3 on 2022-05-18 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_alter_asset_customer_alter_asset_organisation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairingstock',
            name='asset',
            field=models.ForeignKey(db_column='asset_uid', on_delete=django.db.models.deletion.DO_NOTHING, to='assets.asset', to_field='asset_uid'),
        ),
    ]