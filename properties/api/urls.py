from .views import (PropertyListCreateAPIView, PropertyRetrieveUpdateAPIView, MediaManagerAPIView)

from django.urls import path

app_name = 'properties-api'

urlpatterns = [
    path('', PropertyListCreateAPIView.as_view(), name="property_list_create"),
    path('<int:pk>/', PropertyRetrieveUpdateAPIView.as_view(), name="property_detail"),

    # Path for uploading images
    path('media-manager/', MediaManagerAPIView.as_view(), name="media_manager_post"),
    path('media-manager/<str:filename>/', MediaManagerAPIView.as_view(), name="media_manager_delete"),
]
