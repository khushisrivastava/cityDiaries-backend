# Generated by Django 3.1 on 2021-04-14 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200923_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
