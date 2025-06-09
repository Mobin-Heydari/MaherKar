from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAdminOrSupporterOrReporter(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return True

        return True
    

    def has_object_permission(self, request, view, obj):
    
        if request.user.is_staff:
            return True
        
        if request.user == obj.reporter:
            return True
        
        if request.user.user_type == "SU":
            return True
        
        return True
        


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        

        if request.user.is_staff or request.user.user_type == "SU":
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user.is_staff or request.user.user_type == "SU":
            return True
        
        return False