# Generated by Django 2.2.19 on 2021-05-26 07:35

import api_sad_sig.util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0054_auto_20210526_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='saddesa',
            name='gambar_batasdesa',
            field=models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination),
        ),
    ]
