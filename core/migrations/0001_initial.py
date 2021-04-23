# Generated by Django 3.0.8 on 2020-08-19 07:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('gym', 'Gym'), ('restaurant', 'Restaurant'), ('hotel', 'Hotel')], default=None, max_length=10)),
                ('icon', models.TextField(blank=True)),
                ('name', models.CharField(blank=True, max_length=225)),
                ('place_id', models.CharField(max_length=225, unique=True)),
                ('address', models.TextField(blank=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2)),
            ],
            options={
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('gym', 'Gym'), ('restaurant', 'Restaurant'), ('hotel', 'Hotel')], default=None, max_length=10)),
                ('question', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', django.contrib.postgres.fields.jsonb.JSONField()),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_reviews', to='core.Place')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
    ]