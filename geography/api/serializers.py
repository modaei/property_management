from rest_framework.serializers import ModelSerializer
from ..models import Country, City


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'name', ]


class CitySerializer(ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ['id', 'country', 'name', ]
