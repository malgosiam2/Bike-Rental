# Generated by Django 5.1.4 on 2025-01-05 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_order_order_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="order", name="rev_num", field=models.IntegerField(default=None),
        ),
    ]
