from rest_framework import permissions
from authentication.contracts import UserTypes


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.type == UserTypes.MANAGER


class IsManagerOrOwnerOfApplication(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user.type == UserTypes.MANAGER

        return request.user == obj.applicant or request.user.type == UserTypes.MANAGER
