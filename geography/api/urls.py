from django.urls import path
from .views import CountryListAPIView, CityListAPIView

app_name = 'geography-api'

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name="country_list"),
    path('cities/', CityListAPIView.as_view(), name="city_list"),
]
