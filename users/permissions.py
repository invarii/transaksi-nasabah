from django.contrib.auth.models import User, Group
from rest_framework import permissions

SAFE_METHODS = ['GET']


def _is_in_group(user: User, group_name: str):
    return (
        Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    )


def _has_group_permissions(user, required_groups):
    return any(
        _is_in_group(user, group_name) for group_name in required_groups
    )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    rolename = 'admin'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        rolename = request.user.groups.first().name
        return request.method in SAFE_METHODS or rolename == self.rolename


class IsPendudukUserOrReadOnly(permissions.BasePermission):
    rolename = 'penduduk'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        rolename = request.user.groups.first().name
        return request.method in SAFE_METHODS or rolename == self.rolename
