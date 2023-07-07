from rest_framework.permissions import BasePermission
from.models import ClientUsers

class IsActiveClientUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # print()
        if isinstance(user, ClientUsers):
            return user.is_active
        return False