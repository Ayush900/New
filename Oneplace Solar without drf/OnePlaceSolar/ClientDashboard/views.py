from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .permissions import IsActiveClientUser
from .utils import get_tokens_for_user


class YourView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return HttpResponse(f"Hello world {request.user.username}!")
        # Your view logic here
   

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    


    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        print("Data : ",request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_logged_in:
            raise AuthenticationFailed('User is already logged in') 
        user.is_logged_in = True
        
        refresh = RefreshToken.for_user(user)
        user.refresh_token = str(refresh)
        user.access_token = str(refresh.access_token)
        user.save() 
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            })

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print("refresh_token : ",refresh_token)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                # Remove tokens from the database
                BlacklistedToken.objects.filter(token=refresh_token).delete()
                
                # Set is_logged_in to False
                user = request.user
                user.is_logged_in = False
                user.refresh_token = ''
                user.access_token = ''
                user.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
                
            except Exception as e:
                print("Exception : ",e)
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

