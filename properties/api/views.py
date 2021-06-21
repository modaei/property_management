from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from .serializers import (PropertySerializer, PhotoSerializer, )
from ..models import Property, Photo
from rest_framework import status
from .permissions import IsPropertyOwner
from django.core.files.storage import default_storage
from property_management.paginations import PagePagination
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet, BooleanFilter, DateTimeFromToRangeFilter,
                                           CharFilter)
from rest_framework.filters import OrderingFilter
from django.db.models import Count


class PropertyFilter(FilterSet):
    """
    Filter set class for searching in properties
    it can filter based on property name(q), city,
    create_date or the ones that have at least
    one photo
    """
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
    """
    View class for listing, searching and creating properties.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = PagePagination

    def get_queryset(self):
        """
        Just show the properties that the user owns.
        """
        return Property.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the owner of the property before creating it.
        """
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class PropertyRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPropertyOwner]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class MediaManagerAPIView(GenericAPIView):
    """
    View for uploading and deleting property photos.
    Also setting a photo as thumbnail.
    """
    permission_classes = [IsAuthenticated, IsPropertyOwner]
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        """
        Upload new property photo.
        """
        serializer = self.get_serializer(data=request.data)
        # First find the related property object, then check the user permission,
        # if all passes, then assign the new photo to the property
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer_data = serializer.data
            property_ob = Property.objects.get(id=validated_data['property_id'])
            self.check_object_permissions(request, property_ob)
            photo = property_ob.photos.create(image=validated_data['image'], )

            # If the property has no photos or the photo is set to be the thumbnail, set it as thumbnail
            if validated_data['is_thumbnail'] or property_ob.thumbnail_photo is None:
                property_ob.thumbnail_photo = photo
                serializer_data['is_thumbnail'] = True

            return Response(serializer_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete an existing photo of a property
        """
        filename = self.kwargs.get('filename')
        if not filename:
            return Response('filename not specified', status=status.HTTP_400_BAD_REQUEST)

        # Check user's permission. If the user is authorized, check if the photo is set as thumbnail.
        photo = Photo.objects.filter(image=filename).first()
        if photo is not None:
            property_ob = photo.property
            self.check_object_permissions(request, property_ob)
            if property_ob.thumbnail_photo == photo:
                return Response('Image is selected as thumbnail. Please select another image as thumbnail.',
                                status=status.HTTP_400_BAD_REQUEST)

            # Try deleting the related file. Whether successful or not, delete the photo object.
            try:
                img_file = photo.image.file.name
                photo.image = None
                default_storage.delete(img_file)
            except FileNotFoundError:
                photo.image = None
            photo.delete()
            return Response('deleted successfully', status=status.HTTP_200_OK)
        return Response('object not found', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        Sets the specified photo as thumbnail
        """
        filename = self.kwargs.get('filename')
        if not filename:
            return Response('Filename not specified.', status=status.HTTP_400_BAD_REQUEST)

        photo = Photo.objects.filter(image=filename).first()
        # Using the setter defined in the model, sets the property's thumbnail photo.
        if photo is not None:
            property_ob = photo.property
            self.check_object_permissions(request, property_ob)
            property_ob.thumbnail_photo = photo
            return Response('Updated successfully.', status=status.HTTP_200_OK)
        return Response('Object not found.', status=status.HTTP_404_NOT_FOUND)
