from rest_framework.relations import StringRelatedField
from rest_framework.serializers import (ModelSerializer, SerializerMethodField, ValidationError,
                                        BooleanField, IntegerField)
from ..models import Property, Photo
from django.core.files.images import get_image_dimensions
from geography.api.serializers import CitySerializer
from rest_framework.exceptions import NotFound
from easy_thumbnails.files import get_thumbnailer


# This field is able to receive an empty string for an integer field and turn it into a None number
class BlankableIntegerField(IntegerField):
    def to_internal_value(self, data):
        if data == '':
            return None
        return super(BlankableIntegerField, self).to_internal_value(data)


class PropertySerializer(ModelSerializer):
    photos = StringRelatedField(many=True, read_only=True)
    create_date = SerializerMethodField()
    thumbnail = SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'city', 'name', 'description', 'create_date', 'thumbnail', 'photos']
        read_only_fields = ['id', 'create_date', 'photos', 'thumbnail']

    def to_representation(self, instance):
        self.fields['city'] = CitySerializer()
        return super(PropertySerializer, self).to_representation(instance)

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def get_thumbnail(self, obj):
        thumb_photo = obj.thumbnail_photo
        if thumb_photo is None:
            return None
        return get_thumbnailer(thumb_photo.image).get_thumbnail({}).url


class PhotoSerializer(ModelSerializer):
    property_id = IntegerField(required=True)
    is_thumbnail = BooleanField(required=True)

    class Meta:
        model = Photo
        fields = ['image', 'property_id', 'is_thumbnail']

    def validate_image(self, value):
        width, height = get_image_dimensions(value)
        if width < 400 or height < 400:
            raise ValidationError('Image should be at least 400*400 pixels.')
        if value.size > 2 * 1024 * 1024:
            raise ValidationError('File size should be smaller than 2MB.')
        return value

    def validate_property_id(self, value):
        qs = Property.objects.filter(id=value)
        if qs is None or not qs.exists():
            raise NotFound()
        return value

    def validate(self, attrs):
        property_obj = Property.objects.filter(id=attrs['property_id']).first()
        if property_obj is not None:
            if len(property_obj.photos.all()) > 20:
                raise ValidationError('Maximum number of images has already been uploaded.')
        return attrs
