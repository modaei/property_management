from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ValidationError, BooleanField,
                                        IntegerField, )
from django.conf import settings
from ..models import Property, Photo
from django.core.files.images import get_image_dimensions
from geography.api.serializers import CitySerializer
from rest_framework.exceptions import NotFound
from easy_thumbnails.files import get_thumbnailer
from property_management.utils import format_file_size


class PhotoURLSerializer(ModelSerializer):
    """
    Serializes photo objects to valid URLs. Used in GET requests.
    """
    url = SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class PropertySerializer(ModelSerializer):
    """
    Serializes property objects
    """
    photos = PhotoURLSerializer(many=True, read_only=True)
    create_date = SerializerMethodField()
    thumbnail = SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'city', 'name', 'description', 'create_date', 'thumbnail', 'photos']
        read_only_fields = ['id', 'create_date', 'photos', 'thumbnail']

    def to_representation(self, instance):
        """
        Allows to send the city's id as 'city' in PUT and POST (Instead of 'city_id').
        """
        self.fields['city'] = CitySerializer()
        return super(PropertySerializer, self).to_representation(instance)

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_thumbnail(self, obj):
        """
        Creates absolute valid url for the thumbnail photo
        """
        request = self.context.get('request')
        thumb_photo = obj.thumbnail_photo
        if thumb_photo is None:
            return None
        relative_url = get_thumbnailer(thumb_photo.image).get_thumbnail({}).url
        return request.build_absolute_uri(relative_url)


class PhotoSerializer(ModelSerializer):
    """
    Serializer for uploading properties photos.
    """
    property_id = IntegerField(required=True)
    is_thumbnail = BooleanField(required=True)

    class Meta:
        model = Photo
        fields = ['image', 'property_id', 'is_thumbnail']

    def validate_image(self, value):
        """
        Checks width, height and size (volume) of the image.
        """
        width, height = get_image_dimensions(value)
        if width < settings.IMAGE_MIN_WIDTH or height < settings.IMAGE_MIN_HEIGHT:
            raise ValidationError(
                f'Image should be at least {settings.IMAGE_MIN_HEIGHT}*{settings.IMAGE_MIN_WIDTH} pixels.')
        if value.size > settings.IMAGE_MAX_SIZE:
            raise ValidationError(f'File size should be less than {format_file_size(value.size)}.')
        return value

    def validate_property_id(self, value):
        """
        Checks that a property with this property_id exists.
        """
        qs = Property.objects.filter(id=value)
        if qs is None or not qs.exists():
            raise NotFound()
        return value


    def validate(self, attrs):
        """
        Checks the number of uploaded images for a property and
        compares it to the maximum allowed.
        """
        property_obj = Property.objects.filter(id=attrs['property_id']).first()
        if property_obj is not None:
            if len(property_obj.photos.all()) > settings.PROPERTY_MAX_IMAGES:
                raise ValidationError(f'You can not upload more than {settings.PROPERTY_MAX_IMAGES} for a property.')
        return attrs
