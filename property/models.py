from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from geography.models import Country, City


class Photo(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='transportation')
    deleted_image_name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Property(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT,
                                related_name='%(class)s_origin_country')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT,
                             related_name='%(class)s_origin_city')
    title = models.CharField(blank=False, null=False, max_length=30)
    description = models.TextField(blank=False, null=False, max_length=1000)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")
    thumbnail_image = models.CharField(null=True, blank=True, max_length=300)
    thumbnail_photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL)
    photos = GenericRelation(Photo, )
