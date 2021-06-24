from rest_framework.permissions import BasePermission
from rents.models import Tenant
from properties.models import Property


class IsTenantCreatedByUser(BasePermission):
    """
    If the user is the creator of the tenant entity grant access
    otherwise, deny access.
    """
    message = "Only the creator can access this object"

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsLeaseTenantCreatedByUser(BasePermission):
    """
    If the user is the creator of the tenant entity, he
    is allowed to use that tenant for a lease entity.
    """
    message = "You are not allowed to use this tenant."

    def has_permission(self, request, view):
        if request.method != "POST" and request.method != "PUT":
            return True
        tenant = Tenant.objects.get(id=request.data['tenant'])
        if tenant is not None and tenant.creator == request.user:
            return True
        else:
            return False


class IsLeasePropertyOwnedByUser(BasePermission):
    message = "Only the owner can access this lease/use this property."

    def has_permission(self, request, view):
        """
            If the user is the owner of the property entity, he
            is allowed to use that property for a lease entity.
        """
        if request.method != "POST" and request.method != "PUT":
            return True
        new_property = Property.objects.get(id=request.data['property'])
        if new_property is not None and new_property.owner == request.user:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
            If the user is the owner of the property that is
            related to this lease, he is also the owner of
            the lease object, so grant access to this object.
        """
        return obj.property.owner == request.user
