from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'operator'

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'