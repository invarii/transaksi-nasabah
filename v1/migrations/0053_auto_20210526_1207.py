# Generated by Django 2.2.19 on 2021-05-26 05:07

import api_sad_sig.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0052_auto_20210526_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='produk',
            name='gambar2',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
        migrations.AddField(
            model_name='produk',
            name='gambar3',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
        migrations.AddField(
            model_name='produk',
            name='gambar4',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
        migrations.AlterField(
            model_name='produk',
            name='gambar',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
    ]