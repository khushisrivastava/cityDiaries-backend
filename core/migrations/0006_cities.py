# Generated by Django 3.1 on 2020-09-23 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_photos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=2)),
                ('region', models.CharField(blank=True, max_length=3)),
                ('url', models.CharField(blank=True, max_length=225)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('latitude', models.IntegerField(null=True)),
                ('longitude', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
    ]
