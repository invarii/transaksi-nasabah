# Generated by Django 2.2.19 on 2021-03-26 07:11

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    KategoriInformasi = apps.get_model("v1", "KategoriInformasi")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'KategoriInformasi.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        kategori_informasis = []

        for row in reader:
            kategori_informasi = KategoriInformasi(nama=row[1])
            
            kategori_informasis.append(kategori_informasi)

        KategoriInformasi.objects.bulk_create(kategori_informasis)

def reverse_func(apps, schema_editor):
    KategoriInformasi = apps.get_model("v1", "KategoriInformasi")

    KategoriInformasi.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0023_auto_20210326_1408'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]
