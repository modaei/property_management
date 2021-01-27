# Generated by Django 3.1.5 on 2021-01-26 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_auto_20210126_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='title',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(db_index=True, max_length=2, unique=True),
        ),
    ]
