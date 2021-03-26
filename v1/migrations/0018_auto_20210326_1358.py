# Generated by Django 2.2.19 on 2021-03-26 06:58

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    Golongan = apps.get_model("v1", "Golongan")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'golongan.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        golongans = []

        for row in reader:
            golongan = Golongan(nama=row[1])
            
            golongans.append(golongan)

        Golongan.objects.bulk_create(golongans)

def reverse_func(apps, schema_editor):
    Golongan = apps.get_model("v1", "Golongan")

    Golongan.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0017_auto_20210326_1356'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]