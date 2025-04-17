# Generated by Django 4.2.1 on 2024-01-17 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets", "0004_alter_matchaccount_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matchaccount",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="budgets.category"
            ),
        ),
    ]
