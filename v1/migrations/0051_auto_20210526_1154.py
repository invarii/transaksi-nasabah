# Generated by Django 2.2.19 on 2021-05-26 04:54

import api_sad_sig.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0050_auto_20210526_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produk',
            name='gambar',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
    ]
