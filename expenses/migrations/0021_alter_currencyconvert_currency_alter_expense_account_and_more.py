# Generated by Django 4.2.1 on 2024-02-18 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0020_account_account_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyconvert",
            name="currency",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="expenses.currency"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="expenses.account"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="currency",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="expenses.currency"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="period",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="expenses.period"
            ),
        ),
    ]
