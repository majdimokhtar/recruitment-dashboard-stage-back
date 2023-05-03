# Generated by Django 4.1.7 on 2023-03-19 22:08

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0012_remove_job_point"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="point",
            field=django.contrib.gis.db.models.fields.PointField(
                default=django.contrib.gis.geos.point.Point(0.0, 0.0), srid=4326
            ),
        ),
    ]
