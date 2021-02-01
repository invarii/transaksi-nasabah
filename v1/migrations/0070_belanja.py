# Generated by Django 2.2.17 on 2021-01-29 02:29

import api_sad_sig.util
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0069_delete_belanja'),
    ]

    operations = [
        migrations.CreateModel(
            name='Belanja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(blank=True, max_length=20, null=True)),
                ('nama', models.CharField(blank=True, max_length=100, null=True)),
                ('anggaran', models.CharField(blank=True, max_length=100, null=True)),
                ('sumber_dana', models.CharField(blank=True, max_length=100, null=True)),
                ('tgl', models.DateField(blank=True, null=True)),
                ('foto_sebelum', models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination)),
                ('foto_sesudah', models.ImageField(blank=True, null=True, upload_to=api_sad_sig.util.file_destination)),
                ('progres', models.CharField(blank=True, max_length=100, null=True)),
                ('koordinat', models.TextField(blank=True, null=True)),
                ('kategori', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.KategoriBelanja')),
                ('tahun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.KategoriTahun')),
            ],
            options={
                'db_table': 'belanja',
            },
        ),
    ]