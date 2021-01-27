from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import Country, City
from .serializers import CountrySerializer, CitySerializer
from django_filters.rest_framework import (DjangoFilterBackend,
                                           FilterSet,
                                           CharFilter)


class CountryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['country', 'title']


class CityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter
