from rest_framework import permissions

class IsVecino(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.user_type == 1
