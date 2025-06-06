from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAdminOrOwnerForUpdateAndEmployerForCreate(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_staff or request.user.user_type == 'EM'

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff or obj.employer == request.user
