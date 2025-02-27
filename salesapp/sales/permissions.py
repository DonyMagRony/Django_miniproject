# myapp/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework.permissions import IsAuthenticatedOrReadOnly
class TraderOnlyForUnsafe(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user.is_authenticated and request.user.role == 'trader'
