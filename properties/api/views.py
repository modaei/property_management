from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from .serializers import (PropertySerializer, PhotoSerializer, )
from ..models import Property, Photo
from rest_framework import status
from .permissions import IsPropertyOwnerOrReadOnly
from easy_thumbnails.files import get_thumbnailer
from django.core.files.storage import default_storage
from .paginations import PropertyPagePagination
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet, BooleanFilter, DateTimeFromToRangeFilter,
                                           CharFilter)
from rest_framework.filters import OrderingFilter
from django.db.models import Count


class PropertyFilter(FilterSet):
    q = CharFilter(field_name='name', lookup_expr='icontains')
    create_date = DateTimeFromToRangeFilter()
    has_photo = BooleanFilter(field_name='photos', method='filter_with_photos')

    def filter_with_photos(self, queryset, name, value):
        if value:
            return queryset.annotate(photo_count=Count('photos')).filter(photo_count__gt=0)
        else:
            return queryset

    class Meta:
        model = Property
        fields = ['q', 'name', 'city', 'has_photo', 'create_date']


class PropertyListCreateAPIView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = PropertyPagePagination

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class PropertyRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPropertyOwnerOrReadOnly]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class PhotoManagerAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPropertyOwnerOrReadOnly]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            property_ob = Property.objects.get(slug=validated_data['slug'])
            self.check_object_permissions(request, property_ob)
            photo = property_ob.photos.create(image=validated_data['image'], )
            if validated_data['is_thumbnail'] or property_ob.thumbnail_image is None:
                if property_ob.thumbnail_photo:
                    thumbnailer = get_thumbnailer(property_ob.thumbnail_photo.image)
                    thumbnailer.delete_thumbnails()
                property_ob.thumbnail_image = get_thumbnailer(photo.image).get_thumbnail({}).url
                property_ob.thumbnail_photo = photo
                property_ob.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        filename = self.kwargs.get('filename')
        if not filename:
            return Response('filename not specified', status=status.HTTP_400_BAD_REQUEST)

        qs = Photo.objects.filter(image=filename)
        if qs.exists():
            photo = qs.first()
            property_ob = photo.property
            self.check_object_permissions(request, property_ob)
            if property_ob.thumbnail_photo == photo:
                return Response('Image is selected as thumbnail. Please select another image as thumbnail.',
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                img_file = photo.image.file.name
                photo.image = None
                default_storage.delete(img_file)
            except FileNotFoundError:
                # TODO: also check for permission denied. log this error
                photo.image = None
            photo.delete()
            return Response('deleted successfully', status=status.HTTP_200_OK)
        return Response('object not found', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        filename = self.kwargs.get('filename')
        if not filename:
            return Response('filename not specified', status=status.HTTP_400_BAD_REQUEST)

        qs = Photo.objects.filter(image=filename)
        if qs.exists():
            photo = qs.first()
            transportation = photo.content_object
            self.check_object_permissions(request, transportation)
            if transportation.thumbnail_photo:
                thumbnailer = get_thumbnailer(transportation.thumbnail_photo.image)
                thumbnailer.delete_thumbnails()
            transportation.thumbnail_image = get_thumbnailer(photo.image).get_thumbnail({}).url
            transportation.thumbnail_photo = photo
            transportation.save()
            return Response('updated successfully', status=status.HTTP_200_OK)
        return Response('object not found', status=status.HTTP_404_NOT_FOUND)