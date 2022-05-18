# Generated by Django 4.0.3 on 2022-05-18 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
        ('products', '0002_alter_product_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(db_column='organisation_uid', editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='organisations.organisation', to_field='organisation_uid'),
        ),
    ]
