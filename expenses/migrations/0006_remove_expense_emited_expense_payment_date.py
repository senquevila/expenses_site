# Generated by Django 4.2.1 on 2023-07-13 04:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0005_expense_emited"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="emited",
        ),
        migrations.AddField(
            model_name="expense",
            name="payment_date",
            field=models.DateField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
