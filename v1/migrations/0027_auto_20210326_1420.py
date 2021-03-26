# Generated by Django 2.2.19 on 2021-03-26 07:20

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    KeadaanAwal = apps.get_model("v1", "KeadaanAwal")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'keadaan_awal.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        keadaan_awals = []

        for row in reader:
            keadaan_awal = KeadaanAwal(nama=row[1])
            
            keadaan_awals.append(keadaan_awal)

        KeadaanAwal.objects.bulk_create(keadaan_awals)

def reverse_func(apps, schema_editor):
    KeadaanAwal = apps.get_model("v1", "KeadaanAwal")

    KeadaanAwal.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0026_auto_20210326_1416'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]