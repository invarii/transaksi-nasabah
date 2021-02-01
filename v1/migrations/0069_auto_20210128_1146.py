# Generated by Django 2.2.17 on 2021-01-28 04:46

import api_sad_sig.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0068_auto_20210128_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='belanja',
            name='foto_sebelum',
        ),
        migrations.RemoveField(
            model_name='belanja',
            name='foto_sesudah',
        ),
        migrations.RemoveField(
            model_name='suratkeluar',
            name='gambar',
        ),
        migrations.RemoveField(
            model_name='suratmasuk',
            name='gambar',
        ),
        migrations.AddField(
            model_name='suratkeluar',
            name='arsip',
            field=models.FileField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
        migrations.AddField(
            model_name='suratmasuk',
            name='arsip',
            field=models.FileField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
    ]