# Generated by Django 5.0.1 on 2024-09-13 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0018_alter_report_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 13, 16, 12, 34, 460235)),
        ),
    ]
