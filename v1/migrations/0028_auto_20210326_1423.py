# Generated by Django 2.2.19 on 2021-03-26 07:23

from __future__ import unicode_literals

from django.db import migrations
import csv, os
from pathlib import Path

def load_initial_data(apps, schema_editor):
    KelainanFisik = apps.get_model("v1", "KelainanFisik")

    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(os.path.join(os.path.dirname(BASE_DIR), 'v1', 'migrations', 'csv', 'kelainanfisik.csv')) as csv_file:
        reader = csv.reader(csv_file)
        # header = next(reader)

        kelainanfisiks = []

        for row in reader:
            kelainanfisik = KelainanFisik(nama=row[1])
            
            kelainanfisiks.append(kelainanfisik)

        KelainanFisik.objects.bulk_create(kelainanfisiks)

def reverse_func(apps, schema_editor):
    KelainanFisik = apps.get_model("v1", "KelainanFisik")

    KelainanFisik.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0027_auto_20210326_1420'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func)
    ]
