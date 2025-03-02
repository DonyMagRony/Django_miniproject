from rest_framework.permissions import BasePermission

class IsSellerOrAdminForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return request.user.is_authenticated and (request.user.role == 'seller' or request.user.is_staff)

class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user or obj.sales_rep == request.user