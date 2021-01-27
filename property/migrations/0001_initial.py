# Generated by Django 3.1.5 on 2021-01-26 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geography', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='transportation')),
                ('deleted_image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=1000)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Last updated')),
                ('thumbnail_image', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='property_origin_city', to='geography.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='property_origin_country', to='geography.country')),
                ('thumbnail_photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.photo')),
            ],
        ),
    ]
