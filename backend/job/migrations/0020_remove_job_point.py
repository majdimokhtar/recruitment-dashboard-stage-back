# Generated by Django 4.1.7 on 2023-04-03 16:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0019_job_point"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="job",
            name="point",
        ),
    ]