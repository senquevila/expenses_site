# Generated by Django 4.2.1 on 2023-09-18 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0008_period_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currencyconvert",
            name="exchange",
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]