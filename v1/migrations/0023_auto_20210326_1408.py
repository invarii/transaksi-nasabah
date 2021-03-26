# Generated by Django 2.2.19 on 2021-03-26 07:08

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    KategoriArtikel = apps.get_model("v1", "KategoriArtikel")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'KategoriArtikel.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        kategori_artikels = []

        for row in reader:
            kategori_artikel = KategoriArtikel(nama=row[1])
            
            kategori_artikels.append(kategori_artikel)

        KategoriArtikel.objects.bulk_create(kategori_artikels)

def reverse_func(apps, schema_editor):
    KategoriArtikel = apps.get_model("v1", "KategoriArtikel")

    KategoriArtikel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0022_auto_20210326_1407'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]
