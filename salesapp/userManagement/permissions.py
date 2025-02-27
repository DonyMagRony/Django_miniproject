from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to users with the role 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsTrader(BasePermission):
    """
    Allows access only to users with the role 'trader'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trader'

class IsSeller(BasePermission):
    """
    Allows access only to users with the role 'seller'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seller'

class IsCustomer(BasePermission):
    """
    Allows access only to users with the role 'customer'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

