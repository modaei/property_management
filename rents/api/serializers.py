from rest_framework.serializers import (ModelSerializer, SerializerMethodField, )
from ..models import Tenant, Lease


class TenantSerializer(ModelSerializer):
    """
    Serializes Tenant objects
    """
    create_date = SerializerMethodField()

    class Meta:
        model = Tenant

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())


class LeaseSerializer(ModelSerializer):
    """
    Serializes Lease objects
    """
    create_date = SerializerMethodField()

    class Meta:
        model = Lease

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())
