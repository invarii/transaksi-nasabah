# Generated by Django 2.2.19 on 2021-03-26 07:03

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    JenisKelahiran = apps.get_model("v1", "JenisKelahiran")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'jenis_kelahiran.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        jenis_kelahirans = []

        for row in reader:
            jenis_kelahiran = JenisKelahiran(nama=row[1])
            
            jenis_kelahirans.append(jenis_kelahiran)

        JenisKelahiran.objects.bulk_create(jenis_kelahirans)

def reverse_func(apps, schema_editor):
    JenisKelahiran = apps.get_model("v1", "JenisKelahiran")

    JenisKelahiran.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0019_auto_20210326_1400'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]