# Generated by Django 5.1.1 on 2024-09-13 19:31

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0017_report_type_alter_report_date_creation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='police',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 13, 16, 31, 43, 578915)),
        ),
    ]