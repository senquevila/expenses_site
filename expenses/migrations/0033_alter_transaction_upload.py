# Generated by Django 4.2.14 on 2025-02-24 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0032_alter_subscription_subscription_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenses.upload'),
        ),
    ]
