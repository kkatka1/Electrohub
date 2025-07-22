from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение доступа только активным сотрудникам.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_active
