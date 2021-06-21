from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (PropertySerializer, PhotoSerializer, )
from ..models import Property
from .permissions import IsTenantCreator
from .paginations import PropertyPagePagination
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


class TenantListCreateAPIView(ListCreateAPIView):
    """
    View class for listing, searching and creating properties.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = PropertyPagePagination

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


class TenantRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTenantCreator]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
