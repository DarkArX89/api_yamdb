from rest_framework import permissions
from users.models import ADMIN, MODERATOR, USER


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN or request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        return True


class ModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == MODERATOR)

    def has_object_permission(self, request, view, obj):
        return True


class UserORReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == USER)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == USER
                and obj.author == request.user)


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == ADMIN or request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        return True
