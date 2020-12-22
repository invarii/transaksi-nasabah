# Generated by Django 2.2.17 on 2020-12-21 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0041_auto_20201220_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sigbidang',
            name='namabidang',
        ),
        migrations.RemoveField(
            model_name='sigbidang',
            name='pemilik_warga',
        ),
        migrations.AddField(
            model_name='pemiliknonwarga',
            name='namabidang',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='Kepemilikan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namabidang', models.CharField(blank=True, max_length=64, null=True)),
                ('bidang', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='v1.SigBidang')),
                ('penduduk', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='v1.SadPenduduk')),
            ],
        ),
        migrations.AddField(
            model_name='sigbidang',
            name='pemilikwarga',
            field=models.ManyToManyField(through='v1.Kepemilikan', to='v1.SadPenduduk'),
        ),
    ]