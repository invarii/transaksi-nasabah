# Generated by Django 2.2.19 on 2021-02-25 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v1', '0006_merge_20210226_0551'),
    ]

    operations = [
        migrations.CreateModel(
            name='SadDukuh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('nama', models.CharField(blank=True, max_length=70, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_saddukuhs', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='deleted_saddukuhs', to=settings.AUTH_USER_MODEL)),
                ('dusun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.SadDusun')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_saddukuhs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sad_dukuh',
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='sadrw',
            name='dusun',
        ),
        migrations.AlterField(
            model_name='sadpenduduk',
            name='no_hp',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='sigpenggunaantanah',
            name='penggunaan',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='SigPenggunaanWarna',
        ),
        migrations.AddField(
            model_name='sadrw',
            name='dukuh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='v1.SadDukuh'),
        ),
    ]