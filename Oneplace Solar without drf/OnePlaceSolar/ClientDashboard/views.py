from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .permissions import IsActiveClientUser
from .utils import get_tokens_for_user
from .models import ClientUsers, BaseUserManager
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import OutstandingToken


class TestApi(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        x = ClientUsers.objects.all().values(
            'email', 'first_name')
        print("X : ", x)
        return Response(x)
        # Your view logic here


class YourView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return HttpResponse(f"Hello world {request.user.email}!")
        # Your view logic here


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        print("request.user.is_authenticated : ",
              request.user.is_authenticated)
        if user.is_logged_in:
            access_token = OutstandingToken.objects.filter(
                user=user).values('token')
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            print("access_token : ", access_token)

            # access_token = token.access_token
            # Return response indicating that the user is already logged in
            return Response({'detail': 'User is already logged in',
                             'token': str(access_token)
                             }, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        # Set the expiration time of the access token explicitly
        access_token = refresh.access_token
        access_token.set_exp(lifetime=refresh.access_token.lifetime)
        user.is_logged_in = True
        user.save()

        # Update the token expiration time in the user model
        user.token_expires_at = timezone.now(
        ) + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        user.save()

        return Response({'access': str(access_token)}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.is_logged_in = False
            user.save()

            # Log out the user
            logout(request)

            return Response({'message': f'The user {user.email} is being logged out!'}, status=status.HTTP_204_NO_CONTENT)
        except:
            print("Exception : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
