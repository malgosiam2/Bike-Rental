# Generated by Django 5.1.4 on 2025-01-05 01:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_accessoryitem_quantity_bikeitem_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateField(default=datetime.date(2025, 1, 5)),
        ),
    ]
