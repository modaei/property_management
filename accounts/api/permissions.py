from rest_framework.permissions import BasePermission


class IsUserInfoOwner(BasePermission):
    message = "Only the user can view/edit their info"

    def has_object_permission(self, request, view, obj):
        return request.user is obj
