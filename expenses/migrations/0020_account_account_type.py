# Generated by Django 4.2.1 on 2024-02-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0019_period_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="account_type",
            field=models.CharField(
                choices=[("FIX", "Fijo"), ("VAR", "Variable")],
                default="VAR",
                max_length=5,
            ),
        ),
    ]
