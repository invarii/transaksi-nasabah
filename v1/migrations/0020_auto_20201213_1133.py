# Generated by Django 2.2.17 on 2020-12-13 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0019_auto_20201210_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sigbidang',
            name='nbt',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]