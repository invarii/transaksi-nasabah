# Generated by Django 2.2.19 on 2021-03-26 07:33

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    StatusPerkawinan = apps.get_model("v1", "StatusPerkawinan")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'status_perkawinan.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        status_perkawinans = []

        for row in reader:
            status_perkawinan = StatusPerkawinan(nama=row[1])
            
            status_perkawinans.append(status_perkawinan)

        StatusPerkawinan.objects.bulk_create(status_perkawinans)

def reverse_func(apps, schema_editor):
    StatusPerkawinan = apps.get_model("v1", "StatusPerkawinan")

    StatusPerkawinan.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0031_auto_20210326_1431'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]