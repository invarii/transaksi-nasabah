# Generated by Django 2.2.17 on 2021-01-29 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0071_auto_20210129_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absensi',
            name='jumlah',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]