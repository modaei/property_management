from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (TenantSerializer, LeaseSerializer, )
from ..models import Tenant, Lease
from .permissions import IsTenantCreatedByUser, IsLeasePropertyOwnedByUser, IsLeaseTenantCreatedByUser
from property_management.paginations import PagePagination
from django_filters.rest_framework import (DjangoFilterBackend, )
from rest_framework.filters import OrderingFilter


class TenantListCreateAPIView(ListCreateAPIView):
    """
    View class for listing, searching and creating tenants.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    permission_classes = [IsAuthenticated, ]
    serializer_class = TenantSerializer
    pagination_class = PagePagination

    def get_queryset(self):
        """
        Just show the tenants that the user has created.
        """
        return Tenant.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        """
        Set the creator of the tenant before creating it.
        """
        if serializer.is_valid():
            serializer.save(creator=self.request.user)


class TenantRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTenantCreatedByUser]
    serializer_class = TenantSerializer
    queryset = Tenant.objects.all()


class LeaseListCreateAPIView(ListCreateAPIView):
    """
    View class for listing, searching and creating leases.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['create_date']
    ordering = ['-create_date']
    permission_classes = [IsAuthenticated, IsLeaseTenantCreatedByUser]
    serializer_class = LeaseSerializer
    pagination_class = PagePagination

    def get_queryset(self):
        """
        Just show the lease contracts that their related property belongs to the user.
        """
        return Lease.objects.filter(property__owner=self.request.user)


class LeaseRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLeasePropertyOwnedByUser, IsLeaseTenantCreatedByUser]
    serializer_class = LeaseSerializer
    queryset = Lease.objects.all()
