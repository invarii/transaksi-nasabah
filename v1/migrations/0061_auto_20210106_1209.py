# Generated by Django 2.2.17 on 2021-01-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0060_auto_20210106_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sadkelahiran',
            name='waktu_kelahiran',
        ),
        migrations.AddField(
            model_name='sadkelahiran',
            name='jam',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sadkelahiran',
            name='tanggal_kelahiran',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sadkematian',
            name='jam',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sadlahirmati',
            name='jam',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sadkematian',
            name='tanggal_kematian',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sadlahirmati',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True),
        ),
    ]