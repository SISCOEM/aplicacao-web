# Generated by Django 5.0.1 on 2024-10-10 14:42

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Relatório %d/%m/%Y', max_length=256)),
                ('date_creation', models.DateTimeField(default=datetime.datetime(2024, 10, 10, 11, 42, 44, 320088))),
            ],
        ),
        migrations.CreateModel(
            name='Report_field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.TextField(blank=True, default=None, null=True)),
                ('content', models.TextField(blank=True, default=None, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.report')),
            ],
        ),
    ]
