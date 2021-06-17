from rest_framework.permissions import BasePermission, SAFE_METHODS


# If the user is the property's owner grant access
# otherwise, just allow safe methods
class IsPropertyOwnerOrReadOnly(BasePermission):
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


# If the user is the property's owner grant access
# otherwise, deny access.
class IsPropertyOwner(BasePermission):
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
