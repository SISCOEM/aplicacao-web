# Generated by Django 5.1.1 on 2024-09-12 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications_app_mobile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='message',
        ),
    ]
