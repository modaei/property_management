from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTenantCreator(BasePermission):
    """
    If the user is the creator of the tenant entity grant access
    otherwise, deny access.
    """
    message = "Only the creator can access this object"

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
