# Generated by Django 4.2.1 on 2024-01-28 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0017_alter_upload_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="upload",
            name="result",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
