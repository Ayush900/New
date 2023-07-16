from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from .models import ClientUsers
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import OutstandingToken
from django.contrib.auth import logout
from django.utils import timezone


# class CustomIsAuthenticated(IsAuthenticated):
#     def has_permission(self, request, view):
#         has_permission = super().has_permission(request, view)
#         print("Checking if has permission")
#         print("has_permission : ", has_permission)
#         print("request.user.is_authenticated : ",
#               request.user.is_authenticated)

#         if has_permission and request.user.is_authenticated:
#             user = request.user

#             # Get the outstanding tokens for the user
#             print("User : ", user)
#             outstanding_tokens = OutstandingToken.objects.filter(
#                 user=user).values('expires_at')
#             print("outstanding_tokens : ", outstanding_tokens.filter(
#                 expires_at__lte=timezone.now()).exists())

#             # Check if any of the outstanding tokens have expired
#             # print("utstanding_tokens.filter(expires_at__lte=timezone.now()) :",
#             #       outstanding_tokens.filter(expires_at__lte=timezone.now()).expires_at)
#             if outstanding_tokens.filter(expires_at__lte=timezone.now()).exists():
#                 # Perform the necessary actions when a token has expired
#                 user.is_logged_in = False
#                 user.save(update_fields=['is_logged_in'])
#                 print("has_permission", has_permission)
#                 logout(request)
#                 print("has_permission", has_permission)
#                 has_permission = False
#                 user.save()
#                 print("has_permission", has_permission)

#                 # Return False to deny access to the view
#                 return False

#         return has_permission


class IsActiveClientUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        # print()
        if isinstance(user, ClientUsers):
            return user.is_active
        return False
