# Generated by Django 4.2.1 on 2023-09-17 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0007_period_closed"),
    ]

    operations = [
        migrations.AddField(
            model_name="period",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13),
        ),
    ]
