# Generated by Django 5.0.1 on 2025-02-24 05:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('load', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='date_load',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 24, 2, 3, 36, 960545)),
        ),
    ]
