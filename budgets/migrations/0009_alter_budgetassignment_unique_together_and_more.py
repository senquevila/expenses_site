# Generated by Django 4.2.1 on 2024-02-18 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "expenses",
            "0021_alter_currencyconvert_currency_alter_expense_account_and_more",
        ),
        ("budgets", "0008_alter_matchaccount_account_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="budgetassignment",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="budgetassignment",
            name="account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="expenses.account",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="budgetassignment",
            unique_together={("budget", "account")},
        ),
        migrations.DeleteModel(
            name="MatchAccount",
        ),
        migrations.RemoveField(
            model_name="budgetassignment",
            name="category",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]