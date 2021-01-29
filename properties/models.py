from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from geography.models import Country, City


class Property(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(blank=False, null=False, max_length=30)
    description = models.TextField(blank=False, null=False, max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    area = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    address = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")

    thumbnail_image = models.CharField(null=True, blank=True, max_length=300)


class Photo(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='property')
    deleted_image_name = models.CharField(max_length=255, blank=True, null=True)
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.PROTECT)
    is_thumbnail = models.BooleanField(default=False)
