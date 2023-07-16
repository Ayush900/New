
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import ClientUsers


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUsers
        fields = ('email', 'first_name', 'last_name', 'password',
                  'phone_number', 'user_type', 'company_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = ClientUsers.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        return {"message": f"User with mail {instance.email} has been successfully registered."}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print("attrs : ", attrs)
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password')

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
