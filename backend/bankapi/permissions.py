from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class CreateTransactionPermission(BasePermission):
    """
    Only owner of current from_account allows to create transaction
    """

    def has_permission(self, request, view):
        user = request.user
        from_acc = request.data and request.data['from_acc']
        return


class IsAccountAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
