# Generated by Django 4.2.1 on 2024-02-04 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0018_upload_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="period",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]
