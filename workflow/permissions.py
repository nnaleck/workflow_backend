from rest_framework import permissions
from workflow.contracts import UserTypes


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.type == UserTypes.MANAGER
