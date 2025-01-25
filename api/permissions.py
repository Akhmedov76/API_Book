from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Operators').exists()

class IsUser (permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated