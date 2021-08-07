from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPropertyOwnerOrReadOnly(BasePermission):
    """
    If the user is the property's owner grant access
    otherwise, just allow safe methods
    """
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsPropertyOwner(BasePermission):
    """
    If the user is the property's owner grant access
    otherwise, deny access.
    """
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
