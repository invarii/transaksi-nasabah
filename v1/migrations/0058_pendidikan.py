# Generated by Django 2.2.17 on 2021-01-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0057_pekerjaan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pendidikan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'pendidikan',
            },
        ),
    ]