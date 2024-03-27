# permissions.py

from rest_framework.permissions import BasePermission

class IsSiteAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
