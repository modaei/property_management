from rest_framework.relations import HyperlinkedRelatedField, StringRelatedField
from rest_framework.serializers import (ModelSerializer, SerializerMethodField, CharField, ValidationError,
                                        BooleanField, IntegerField)
from ..models import Property, Photo
from django.core.files.images import get_image_dimensions
from geography.api.serializers import CitySerializer


# This field is able to receive an empty string for an integer field and turn it into a None number
class BlankableIntegerField(IntegerField):
    def to_internal_value(self, data):
        if data == '':
            return None
        return super(BlankableIntegerField, self).to_internal_value(data)


class PropertySerializer(ModelSerializer):
    photos = StringRelatedField(many=True, read_only=True)
    create_date = SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'city', 'name', 'description', 'create_date', 'thumbnail_image', 'photos']
        read_only_fields = ['id', 'create_date', 'photos', 'thumbnail_image']

    def to_representation(self, instance):
        self.fields['city'] = CitySerializer()
        return super(PropertySerializer, self).to_representation(instance)

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())


class PhotoSerializer(ModelSerializer):
    object_type = CharField(required=True)
    slug = CharField(required=True)
    is_thumbnail = BooleanField(required=False)

    class Meta:
        model = Photo
        fields = ['image', 'slug', 'is_thumbnail']

    def validate_image(self, value):
        width, height = get_image_dimensions(value)
        if width < 400 or height < 400:
            raise ValidationError('Image should be at least 400*400 pixels.')
        if value.size > 2 * 1024 * 1024:
            raise ValidationError('File size should be smaller than 2MB.')
        return value

    def validate(self, attrs):
        qs = Property.objects.filter(slug=attrs['slug'])

        if qs is None or not qs.exists():
            raise ValidationError('Specified object does not exist.')
        photos = qs.first().photos.all()
        if len(photos) >= 6:
            raise ValidationError('Maximum number of images are already uploaded.')
        return attrs
