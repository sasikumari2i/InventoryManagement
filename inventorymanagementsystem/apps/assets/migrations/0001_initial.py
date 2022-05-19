# Generated by Django 4.0.3 on 2022-05-18 03:35

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("organisations", "0001_initial"),
        ("orders", "__first__"),
        ("products", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "asset_uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "[A-Za-z]+([ ][a-zA-Z]+)*", "Enter a valid name"
                            )
                        ],
                    ),
                ),
                ("created_date", models.DateField(default=datetime.date.today)),
                ("updated_date", models.DateField(default=datetime.date.today)),
                ("serial_no", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("return_date", models.DateField(default=None, null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="orders.customer",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="organisations.organisation",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="products.product",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="RepairingStock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                (
                    "repairing_stock_uid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("serial_no", models.CharField(max_length=100)),
                ("created_date", models.DateField(default=datetime.date.today)),
                ("updated_date", models.DateField(default=datetime.date.today)),
                ("closed_date", models.DateField(default=None, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="assets.asset",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="organisations.organisation",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="products.product",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
