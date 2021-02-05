# Generated by Django 2.2.17 on 2021-02-03 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0077_statuslapor_warna'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kepemilikanwarga3',
            name='bidang',
        ),
        migrations.RemoveField(
            model_name='kepemilikanwarga3',
            name='penduduk',
        ),
        migrations.RemoveField(
            model_name='sadkeluarga3',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sadkeluarga3',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='sadkeluarga3',
            name='dusun',
        ),
        migrations.RemoveField(
            model_name='sadkeluarga3',
            name='menguasai',
        ),
        migrations.RemoveField(
            model_name='sadkeluarga3',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='dusun',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='pemiliknonwarga',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='pemilikwarga',
        ),
        migrations.RemoveField(
            model_name='sigbidang3',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='sigpemilik3',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sigpemilik3',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='sigpemilik3',
            name='pemilik',
        ),
        migrations.RemoveField(
            model_name='sigpemilik3',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='KepemilikanNonWarga3',
        ),
        migrations.DeleteModel(
            name='KepemilikanWarga3',
        ),
        migrations.DeleteModel(
            name='PemilikNonWarga3',
        ),
        migrations.DeleteModel(
            name='SadKeluarga3',
        ),
        migrations.DeleteModel(
            name='SigBidang3',
        ),
        migrations.DeleteModel(
            name='SigPemilik3',
        ),
    ]