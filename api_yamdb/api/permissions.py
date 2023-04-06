from rest_framework import permissions


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ADMIN or request.user.is_staff))


class ModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == MODERATOR)


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


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == ADMIN or request.user.is_staff
                or request.user.role == MODERATOR
                or request.user == obj.author)
