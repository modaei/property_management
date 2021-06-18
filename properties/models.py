from django.db import models
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from geography.models import City
import ntpath


class Property(models.Model):
    """
    Represents a real estate property.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(blank=False, null=False, max_length=30, db_index=True)
    description = models.TextField(blank=True, null=True, max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    area = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    address = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")
    thumbnail_image = models.CharField(null=True, blank=True, max_length=300, db_index=True)

    @property
    def thumbnail_photo(self):
        """
        This property is used to return property's thumbnail image.
        """
        return self.photos.filter(is_thumbnail=True).first()

    @thumbnail_photo.setter
    def thumbnail_photo(self, photo):
        """
        Setter for updating the thumbnail photo of a property.
        """
        # If the property already has a thumbnail, remove it and mark the related photo as not thumbnail.
        if self.thumbnail_photo:
            thumbnailer = get_thumbnailer(self.thumbnail_photo.image)
            thumbnailer.delete_thumbnails()

            # Set the is_thumbnail attribute of the related Photo object to false.
            thumb_photo = Photo.objects.get(id=self.thumbnail_photo.id)
            thumb_photo.is_thumbnail = False
            thumb_photo.save()

        # Now create the thumbnail and save its path in the property object
        self.thumbnail_image = ntpath.basename(get_thumbnailer(photo.image).get_thumbnail({}).file.name)
        self.save()

        # Set the photo as thumbnail.
        photo.is_thumbnail = True
        photo.save()

    def __str__(self):
        return self.name


class Photo(models.Model):
    """
    Represents an uploaded image for a property
    """
    image = models.ImageField(null=True, blank=True, db_index=True)
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.PROTECT)
    is_thumbnail = models.BooleanField(default=False)
