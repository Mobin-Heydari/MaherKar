from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows read-only access to anyone,
    but restricts write operations to admin users only.
    """
    message = "Only admin users are allowed to create, update, or delete data."

    def has_permission(self, request, view):
        # Allow read-only methods for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, ensure the user is an admin.
        return request.user and request.user.is_staff