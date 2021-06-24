# Generated by Django 3.1.5 on 2021-06-22 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import property_management.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0013_auto_20210622_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=255, validators=[property_management.validators.validate_names])),
                ('last_name', models.CharField(max_length=255, validators=[property_management.validators.validate_names])),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True, validators=[property_management.validators.validate_phone_number])),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deposit', models.PositiveIntegerField()),
                ('rent', models.PositiveIntegerField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='properties.property')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rents.tenant')),
            ],
        ),
    ]
