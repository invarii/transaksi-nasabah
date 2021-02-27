# Generated by Django 2.2.19 on 2021-02-27 04:46

import api_sad_sig.util
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0009_delete_potensi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Potensi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_usaha', models.CharField(blank=True, max_length=100, null=True)),
                ('harga', models.CharField(blank=True, max_length=100, null=True)),
                ('jenis_promosi', models.CharField(blank=True, max_length=100, null=True)),
                ('no_telp', models.CharField(blank=True, max_length=100, null=True)),
                ('judul', models.CharField(blank=True, max_length=100, null=True)),
                ('isi', models.TextField(blank=True, null=True)),
                ('koordinat', models.TextField(blank=True, null=True)),
                ('gambar', models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination)),
                ('kategori', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.KategoriPotensi')),
            ],
            options={
                'db_table': 'Potensi',
            },
        ),
    ]
