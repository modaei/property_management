from rest_framework.serializers import (ModelSerializer, SerializerMethodField, )

from properties.api.serializers import PropertySerializer
from ..models import Tenant, Lease


class TenantSerializer(ModelSerializer):
    create_date = SerializerMethodField()

    class Meta:
        model = Tenant
        fields = ['id', 'create_date', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'create_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())


class LeaseSerializer(ModelSerializer):
    create_date = SerializerMethodField()

    class Meta:
        model = Lease
        fields = ['id', 'property', 'start_date', 'end_date', 'deposit', 'rent', 'create_date', 'tenant']
        read_only_fields = ['id', 'create_date']

    def get_create_date(self, obj):
        return int(obj.create_date.timestamp())

    def to_representation(self, instance):
        """
        Allows to send the property and tenant's id as 'property' and
        'tenant' in PUT and POST (Instead of 'property_id' and 'tenant_id').
        """
        self.fields['property'] = PropertySerializer()
        self.fields['tenant'] = TenantSerializer()
        return super(LeaseSerializer, self).to_representation(instance)
