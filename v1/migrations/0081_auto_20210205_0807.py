# Generated by Django 2.2.17 on 2021-02-05 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0080_absensi_alasanizin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alamat',
            old_name='alamat',
            new_name='jalan_blok',
        ),
    ]