# Generated by Django 5.0.1 on 2024-08-13 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0012_alter_report_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 13, 10, 34, 35, 547186)),
        ),
    ]
