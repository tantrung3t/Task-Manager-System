
import random
from shutil import ReadError
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from user.models import User, Mode, Pin
from django.contrib.auth import authenticate
from .serializers import ModeSerializer, UserSerializer, MyTokenObtainPairSerializer, ProfileSerializer
from .serializers import ChangePasswordSerializer, PinSerializer, ChangePasswordWithPinSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens


# Create your views here.

class LoginApiView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# class RegisterApiView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


class RegisterApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        self.user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        new_user = User.objects.get(email=request.data['email'])
        # Init mode for new user
        mode = {
            "user": new_user.id,
        }
        serializer = ModeSerializer(data=mode)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #
        refresh = tokens.RefreshToken.for_user(self.user)
        refresh['email'] = request.data['email']
        data = {
            "response": response.data,
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class ForgotPasswordApiView(APIView):

    def create_pin(self, user):
        pin = random.randint(100000, 999999)
        data = {
            'user': user.id,
            'pin': pin
        }
        # Tạo hoặc làm mới mã pin
        try:
            pin_user = Pin.objects.get(user = user.id)
            serializer = PinSerializer(instance=pin_user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            serializer = PinSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save() 
        return pin

    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
        except:
            return Response({"message": "Nè email " + request.data['email'] + " này có đăng ký đâu mà lấy lại mật khẩu?"}, status=status.HTTP_404_NOT_FOUND)
        
        pin_code = self.create_pin(user)

        html_content = render_to_string("index.html", {'fullname': user.fullname, 'pin': pin_code})
        send_mail(
            subject='Task Manager System - Forgot Password',
            message='Mật khẩu mới nè cha nội',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data["email"]],
            html_message=html_content
        )
        return Response({"message": "Nè " + user.fullname + " có cái mật khẩu cũng không nhớ gửi qua email mật khẩu mới rồi đó."})


class ProfileApiView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializers = UserSerializer(request.user)
        data = {
            "profile": serializers.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request):
        user_id = request.user.id
        queryset = User.objects.get(pk=user_id)
        serializers = ProfileSerializer(queryset, request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(data=serializers.data, status=status.HTTP_200_OK)


class ModeApiView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        instance = Mode.objects.get(user = request.user.id)
        return Response(data={"mode": instance.mode})

    def put(self, request):
        instance = Mode.objects.get(user = request.user.id)
        data = {
            "user": request.user.id,
            "mode": request.data["mode"]
        }
        serializer = ModeSerializer(instance, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()   

        return Response(data=serializer.data)


class ChangePasswordApiView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            # Hash new password and save new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'Success',
                'message': 'Password change successfully',
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordWithPINApiView(APIView):
    
    def disable_pin(self):
        self.pin.delete()

    def put(self, request):

        serializers = ChangePasswordWithPinSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            self.user = User.objects.get(email = request.data['email'])
            self.pin = Pin.objects.get(user = self.user.id)

            if int(request.data['pin']) == int(self.pin.pin):
                self.user.set_password(request.data['new_password'])
                self.user.save()
                self.disable_pin()
                return Response(data={"message" : "Change password is success"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"message" : "Is valid PIN code"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data = {'message': "Account not found or No forgot password"}, status=status.HTTP_400_BAD_REQUEST)