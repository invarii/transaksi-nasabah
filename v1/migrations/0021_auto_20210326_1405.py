# Generated by Django 2.2.19 on 2021-03-26 07:05

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    JenisTempat = apps.get_model("v1", "JenisTempat")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'jenis_tempat.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        jenis_tempats = []

        for row in reader:
            jenis_tempat = JenisTempat(nama=row[1])
            
            jenis_tempats.append(jenis_tempat)

        JenisTempat.objects.bulk_create(jenis_tempats)

def reverse_func(apps, schema_editor):
    JenisTempat = apps.get_model("v1", "JenisTempat")

    JenisTempat.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0020_auto_20210326_1403'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]
