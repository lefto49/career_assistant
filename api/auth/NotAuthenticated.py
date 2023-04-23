from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    """Checks whether the user is not authenticated."""
    def has_permission(self, request, view):
        return not request.user.is_authenticated
