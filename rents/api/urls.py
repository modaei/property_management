from .views import (TenantListCreateAPIView, TenantRetrieveUpdateDestroyAPIView, LeaseRetrieveUpdateAPIView,
                    LeaseListCreateAPIView)

from django.urls import path

app_name = 'rents-api'

urlpatterns = [
    path('tenants/', TenantListCreateAPIView.as_view(), name="tenant_list_create"),
    path('tenants/<int:pk>/', TenantRetrieveUpdateDestroyAPIView.as_view(), name="tenant_detail_update"),

    path('leases/', LeaseListCreateAPIView.as_view(), name="tenant_list_create"),
    path('leases/<int:pk>/', LeaseRetrieveUpdateAPIView.as_view(), name="tenant_detail_update"),
]
