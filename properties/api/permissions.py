from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPropertyOwnerOrReadOnly(BasePermission):
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsPropertyOwner(BasePermission):
    message = "Only the owner can edit/delete this object"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
