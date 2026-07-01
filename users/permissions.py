from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Дозвіл тільки для адміністраторів"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsOwnerOrAdmin(BasePermission):
    """Дозвіл для власника або адміністратора"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.user == request.user