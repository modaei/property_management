# Generated by Django 3.1.5 on 2021-01-30 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_auto_20210130_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='thumbnail_photo',
        ),
    ]