# Generated by Django 4.2.5 on 2023-12-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0005_alter_police_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='police',
            name='fingerprint',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
