# Generated by Django 2.2.17 on 2021-01-07 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0064_auto_20210107_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sadkelahiran',
            name='nama',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkelahiran',
            name='nama_ayah',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkelahiran',
            name='nama_ibu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkelahiran',
            name='nama_pelapor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkematian',
            name='nama_pelapor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkematian',
            name='nama_saksi_dua',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadkematian',
            name='nama_saksi_satu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadlahirmati',
            name='nama_ayah',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadlahirmati',
            name='nama_ibu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadlahirmati',
            name='nama_pelapor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadpenduduk',
            name='nama_ayah',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sadpenduduk',
            name='nama_ibu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]