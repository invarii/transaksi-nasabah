# Generated by Django 2.2.17 on 2020-12-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0042_auto_20201221_2255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='potensi',
            old_name='bidang',
            new_name='alamat',
        ),
        migrations.RenameField(
            model_name='potensi',
            old_name='centroid',
            new_name='koordinat',
        ),
        migrations.RemoveField(
            model_name='potensi',
            name='geometry',
        ),
        migrations.AddField(
            model_name='potensi',
            name='jenis_promosi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='potensi',
            name='nama_usaha',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
