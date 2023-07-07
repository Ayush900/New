
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import ClientUsers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUsers
        fields = ('email', 'first_name', 'last_name', 'password','username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("validated_data : ",validated_data)
        user = ClientUsers.objects.create_user(**validated_data)

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print("attrs : ",attrs)
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password')

        attrs['user'] = user
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
