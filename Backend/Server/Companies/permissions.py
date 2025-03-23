from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsAdminOrOwnerForUpdateAndEmployerForCreate(BasePermission):
    """
    Custom permission to allow:
    - Only employer users to create a company.
    - Only admin users and the company owner (employer) to update a company.
    """

    def has_permission(self, request, view):
        # Allow all users to perform safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # For CREATE (POST), only employer users can create companies
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.user_type == 'EM'

        return True

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        - For UPDATE (PUT, PATCH), only admins and company owners (employers) are allowed.
        """
        # Allow safe methods for all
        if request.method in SAFE_METHODS:
            return True

        # Allow only admins or the company owner to update
        if request.method in ('PUT'):
            return request.user.is_authenticated and (
                request.user.is_admin or obj.employer == request.user
            )

        return False
