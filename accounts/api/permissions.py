from rest_framework.permissions import BasePermission


class IsUserInfoOwner(BasePermission):
    """
    If the user is trying to edit his own account's information
    grant access, otherwise deny.
    """
    message = "Only the user can view/edit their info"

    def has_object_permission(self, request, view, obj):
        return request.user is obj
