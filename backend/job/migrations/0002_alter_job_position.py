# Generated by Django 4.1.7 on 2023-02-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="position",
            field=models.IntegerField(default=1),
        ),
    ]
