# Generated by Django 4.2.1 on 2024-01-15 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0012_accountasociation"),
        ("budgets", "0003_matchaccount"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="matchaccount",
            unique_together={("category", "account")},
        ),
    ]
