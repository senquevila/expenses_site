# Generated by Django 4.2.1 on 2023-07-09 07:21

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0004_rename_currencyconvertion_currencyconvert_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="emited",
            field=models.DateField(
                blank=True, default=datetime.date(2023, 7, 9), null=True
            ),
        ),
    ]
