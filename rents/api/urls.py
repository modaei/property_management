from .views import (TenantListCreateAPIView, TenantRetrieveUpdateAPIView)

from django.urls import path

app_name = 'rents-api'

urlpatterns = [
    path('', TenantListCreateAPIView.as_view(), name="tenant_list_create"),
    path('<int:pk>/', TenantRetrieveUpdateAPIView.as_view(), name="tenant_detail_update"),
]
