# Generated by Django 4.2.1 on 2024-01-15 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0012_accountasociation"),
        ("budgets", "0002_alter_budget_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchAccount",
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
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="expenses.account",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budgets.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Categorizacion de gasto",
                "verbose_name_plural": "Categorizaciones de gastos",
            },
        ),
    ]