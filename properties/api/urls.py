from .views import (PropertyListCreateAPIView, PropertyRetrieveUpdateAPIView, PhotoManagerAPIView)

from django.urls import path

app_name = 'property-api'

urlpatterns = [
    path('', PropertyListCreateAPIView.as_view(), name="property_list_create"),
    path('property/<int:id>/', PropertyRetrieveUpdateAPIView.as_view(), name="property_detail"),

    path('photo-manager/', PhotoManagerAPIView.as_view(), name="photo_manager_post"),
    path('photo-manager/<str:filename>/', PhotoManagerAPIView.as_view(), name="photo_manager_delete"),
    path('set-thumbnail/<str:filename>/', PhotoManagerAPIView.as_view(), name="photo_manager_set_thumb"),
]
