
from dataclasses import field, fields
from importlib.metadata import requires
from pyexpat import model
from user.models import User, Mode, Pin
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'fullname']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token


class ModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode 
        fields = ['user', 'mode']

class ChangePasswordSerializer(serializers.Serializer):

    # model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ['user', 'pin']

class ChangePasswordWithPinSerializer(serializers.Serializer):

    # model = User
    email = serializers.EmailField(required=True)
    pin = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)