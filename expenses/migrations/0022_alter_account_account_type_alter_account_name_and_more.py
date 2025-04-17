# Generated by Django 4.2.1 on 2024-03-02 19:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import expenses.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "expenses",
            "0021_alter_currencyconvert_currency_alter_expense_account_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_type",
            field=models.CharField(
                choices=[("FIX", "Fijo"), ("VAR", "Variable")],
                default="VAR",
                max_length=5,
                verbose_name="Tipo de cuenta",
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="account",
            name="sign",
            field=models.IntegerField(
                choices=[(-1, "Debe (-)"), (1, "Haber (+)")], verbose_name="Signo"
            ),
        ),
        migrations.AlterField(
            model_name="accountasociation",
            name="token",
            field=models.CharField(max_length=100, verbose_name="Token para asociar"),
        ),
        migrations.AlterField(
            model_name="currency",
            name="alpha3",
            field=models.CharField(
                blank=True, max_length=3, null=True, verbose_name="Codigo alpha-3"
            ),
        ),
        migrations.AlterField(
            model_name="currency",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="currencyconvert",
            name="date",
            field=models.DateField(
                auto_now_add=True, verbose_name="Fecha de conversión"
            ),
        ),
        migrations.AlterField(
            model_name="currencyconvert",
            name="exchange",
            field=models.DecimalField(
                decimal_places=4, max_digits=10, verbose_name="Tasa de conversión"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, max_digits=13, verbose_name="Monto"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="description",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Descripción"
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="local_amount",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                editable=False,
                max_digits=13,
                verbose_name="Monto local",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="payment_date",
            field=models.DateField(
                blank=True,
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Fecha de pago",
            ),
        ),
        migrations.AlterField(
            model_name="period",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Es visible"),
        ),
        migrations.AlterField(
            model_name="period",
            name="closed",
            field=models.BooleanField(default=False, verbose_name="Solo lectura"),
        ),
        migrations.AlterField(
            model_name="period",
            name="month",
            field=models.IntegerField(verbose_name="Mes"),
        ),
        migrations.AlterField(
            model_name="period",
            name="total",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=13, verbose_name="Monto total"
            ),
        ),
        migrations.AlterField(
            model_name="period",
            name="year",
            field=models.IntegerField(verbose_name="Año"),
        ),
        migrations.AlterField(
            model_name="upload",
            name="file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=expenses.models.expense_upload_path,
                verbose_name="Archivo",
            ),
        ),
        migrations.AlterField(
            model_name="upload",
            name="lines",
            field=models.IntegerField(default=0, verbose_name="Número de líneas"),
        ),
        migrations.AlterField(
            model_name="upload",
            name="result",
            field=models.JSONField(blank=True, null=True, verbose_name="Resultado"),
        ),
        migrations.CreateModel(
            name="UploadData",
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
                ("json", models.JSONField()),
                (
                    "upload",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="expenses.upload",
                    ),
                ),
            ],
        ),
    ]
