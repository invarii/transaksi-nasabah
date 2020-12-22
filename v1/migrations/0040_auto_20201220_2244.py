# Generated by Django 2.2.17 on 2020-12-20 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0039_auto_20201220_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sigbidang',
            name='penguasa',
        ),
        migrations.AddField(
            model_name='sadkeluarga',
            name='menguasai',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.SigBidang'),
        ),
        migrations.AddField(
            model_name='sigbidang',
            name='penguasa_nonwarga',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.RemoveField(
            model_name='sigbidang',
            name='pemilik_warga',
        ),
        migrations.AddField(
            model_name='sigbidang',
            name='pemilik_warga',
            field=models.ManyToManyField(blank=True, null=True, to='v1.SadPenduduk'),
        ),
    ]